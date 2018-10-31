from flask import Flask, jsonify, json, request, abort
from flask_restplus import Resource, Api
from models.models import FastTextModel, Wikipedia2VecModel
from downloader import Downloader
from celery import Celery
import os
import config
import textacy
import textacy.keyterms as tck

app = Flask(__name__)
app.config.from_pyfile('config.py')
api = Api(app)

Downloader(app)
celery = Celery(app)
#celery.conf.update(app.config)

#preloading models
try:
    model_fasttext_scopus = FastTextModel(app.config["FASTTEXT_FILE_MODEL_SCOPUS"])
    wikipedia2vec_models_en = Wikipedia2VecModel(
        'en', app.config["WIKIPEDIA2VEC_EMBEDDINGS_EN"], app.config["WIKIPEDIA2VEC_DIC_EN"], app.config["WIKIPEDIA2VEC_MENTION_EN"])
#    model_fasttext_pf = FastTextModel(app.config["FASTTEXT_FILE_MODEL_PF"])
except Exception as e :
    app.logger.error(e)

MAPPING_MODELS = {
    'scopus': model_fasttext_scopus,
    'wiki2vec_en': wikipedia2vec_models_en
    #'pf': model_fasttext_pf
}

class TextacyFormatting(object):
    """
    Format incoming data to be processed by textacy and extract keyterms.
    """
    def __init__(self, data, lang=None):
        self.data = data
        self.lang = self._detect_lang(data['text']) if not lang else lang
        if 'method' in data:
            self.method = data['method']
        else:
            self.method = 'sgrank'

    def _detect_lang(self, text):
            return textacy.text_utils.detect_language(text)

    def _apply_keyterm_ranking(self, doc, params=None):
        if self.method == 'sgrank':
            keywords = textacy.keyterms.sgrank(doc, **params) \
                if params else tck.sgrank(doc)
        elif self.method == 'textrank':
            keywords = textacy.keyterms.textrank(doc, **params) \
                if params else tck.textrank(doc)
        elif self.method == 'singlerank':
            keywords = textacy.keyterms.singlerank(doc, **params) \
                if params else tck.singlerank(doc)
        return keywords

    def get_keyterms(self, params=None):
        doc = textacy.Doc(self.data['text'], lang=self.lang)
        keywords = self._apply_keyterm_ranking(doc, params)
        return keywords


@api.route('/keywords')
class TextacyResponse(Resource):
    def post(self):
        data = request.json
        params = data.get('params')
        if data is None or 'text' not in data:
            abort(400, "No parameter text was founds. Default JSON input is : {'text':...}")
        else:
            tc = TextacyFormatting(data, lang=data.get('lang'))
            try:
                keywords = tc.get_keyterms(params=params)
                return {'keywords': keywords}, 200
            except Exception as e:
                abort(400, e)   


@api.route('/predictions_fasttext')
class FastTextResponse(Resource):
    def post(self):
        data = request.json
        app.logger.debug('test')
        try:
            m = MAPPING_MODELS[data['model']]
            k = int(data.get('k')) if data.get('k') else 1
            threshold = float(data.get('threshold')
                        ) if data.get('threshold') else 0.0
            labels = list(map(lambda x: {'label': x['label'].replace('__label__', '')
                                             .replace('_', ' '),
                                     'probas': x['probas']},
                        m.make_prediction(data, k, threshold)))
            return jsonify({"labels": labels})
        except Exception as e:
            abort(400, e)


@api.route('/entity_linking')
class Wikipedia2VecResponse(Resource):
    def post(self):
        data = request.json
        try:
            model = MAPPING_MODELS['wiki2vec_en']
            response = model.detect_mentions(data['text'])
            return jsonify(response)
        except Exception as e:
            abort(400, e)


@api.route('/restart_downloader')
class RestartDownloader(Resource):
    def get(self):
        downloaded = Downloader(app)
        if os.path.exists(downloaded.download_dir):
            return {'info': 'Data is present'}, 200
        else:
            return {'info': 'Failed to download data'}, 500

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
