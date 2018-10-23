from flask import Flask, json, request, abort
from flask_restplus import Resource, Api
from models import FastTextModel
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
        app.logger.debug(request.json)
        if data is None or 'text' not in data:
            abort(400, "No parameter text was founds. Default JSON input is : {'text':...}")
        else:
            tc = TextacyFormatting(data, lang=data.get('lang'))
            try:
                keywords = tc.get_keyterms()
                return {'keywords': keywords}, 200
            except Exception as e:
                abort(400, e)   


@api.route('/predictions_fasttext')
class FastTextResponse(Resource):
    def post(self):
        data = request.json
        # formatting data to extract keywords
        tc = TextacyFormatting(data, lang=data.get('lang'))
        keywords = tc.get_keyterms(params=data.get('params'))

        model = FastTextModel(app.config["FASTTEXT_FILE_MODEL_SCOPUS"])

        k = int(request.args.get('k')) if request.args.get('k') else 1
        threshold = float(request.args.get('threshold')
                    ) if request.args.get('threshold') else 0.0
        queries = [{'text': s[0]} for s in keywords]
        response = [model.make_prediction(q, k, threshold) for q in queries]
        return json.dumps(response)


@api.route('/entity_linking', methods=["POST"])
class Wikipedia2VecResponse(Resource):
    def __init__(self):
        self.models = {}
    def post(self):
        lang = request.args.get('lang') if request.args.get('lang') else 'en'
        queries = request.json


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
