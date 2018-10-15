from flask import Flask, json, request, abort
from flask_restplus import Resource, Api
from models import FastTextModel
import textacy
import textacy.keyterms as tck

app = Flask(__name__)
app.config.from_object('Config.Config')
api = Api(app)


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
        doc = textacy.Doc(self.data['text'].decode('utf-8'), lang=self.lang)
        keywords = self._apply_keyterm_ranking(doc, params)
        return keywords


@api.route('/keywords')
class TextacyResponse(Resource):
    def post(self):
        data = request.json
        if 'text' not in data:
            abort(400, "No parameter text was founds.")
        else:
            tc = TextacyFormatting(data, lang=data.get('lang'))        
            try:
                keywords = tc.get_keyterms()
                return {'keywords': keywords}, 200
            except Exception as e:
                abort(400, e)   


@api.route('/predictions_fasttext', methods=["POST"])
class FastTextResponse(Resource):
    def __init__(self):
        self.model = FastTextModel(app.config["fastText_file"])
    def post(self):
        data = request.json
        k = int(request.args.get('k')) if request.args.get('k') else 1
        threshold = float(request.args.get('threshold')
                    ) if request.args.get('threshold') else 0.0
        queries = json.loads(request.data)
        response = [self.model.make_prediction(q, k, threshold) for q in queries]
        return json.dumps(response)

if __name__ == '__main__':
    app.run(debug=True)
