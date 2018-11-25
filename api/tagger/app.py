from flask import Flask, jsonify, json, request, abort
from flask_restplus import Resource, Api
from models import FastTextModel, Wikipedia2VecModel
import os
import textacy
import textacy.keyterms as tck

app = Flask(__name__)
app.config.from_pyfile('config.py')
api = Api(app)


#preloading models
try:
    model_fasttext_scopus = FastTextModel(app.config["FASTTEXT_FILE_MODEL_SCOPUS"])
    wikipedia2vec_models_en = Wikipedia2VecModel(
        'en', app.config["WIKIPEDIA2VEC_DIC_EN"], app.config["WIKIPEDIA2VEC_MENTION_EN"])
    wikipedia2vec_models_fr = Wikipedia2VecModel(
        'fr', app.config["WIKIPEDIA2VEC_DIC_FR"], app.config["WIKIPEDIA2VEC_MENTION_FR"])
    model_fasttext_pf = FastTextModel(app.config["FASTTEXT_FILE_MODEL_PF"])

    MAPPING_MODELS = {
        'scopus': model_fasttext_scopus,
        'wiki2vec_en': wikipedia2vec_models_en,
        'wiki2vec_fr':  wikipedia2vec_models_fr,
        'pf': model_fasttext_pf
    }
except Exception as e :
    app.logger.error(e)


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
        lang = data.get('lang')
        try:
            if lang:
                name_model = 'wiki2vec_{}'.format(lang)
                model = MAPPING_MODELS[name_model]
            else:
                model = MAPPING_MODELS['wiki2vec_en']
            response = model.detect_mentions(data['text'])
            return jsonify(response)
        except Exception as e:
            abort(400, e)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
