from textacy.datasets import Wikipedia
from textacy.io import split_records
from textacy import Vectorizer, Corpus
import io

def load_vectors(fname):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    for line in fin:
        tokens = line.rstrip().split(' ')
        data[tokens[0]] = map(float, tokens[1:])
    return data

class TextacyCorpusWikipedia(object):
    def __init__(self, lang, version='latest'):
        self.lang = lang
        self.wp = Wikipedia(lang, version=version)
        self.wp.download()
        self.build_corpus()

    def build_corpus(self):
        texts = self.wp.records()
        text_stream, metadata_stream = split_records(texts, 'text')
        self.corpus = Corpus(self.lang, texts= text_stream, metadatas=metadata_stream)

class TfidfEmbeddingVectorizer(object):
    """
    Building tfidf weighted scheme out of a textacy Corpus.
    """
    def __init__(self, w2v, corpus, total_doc=100):
        self.w2v = w2v
        self.corpus = corpus
        self.total_doc = total_doc
        self.vectorizer = Vectorizer(
                            apply_idf=True, norm='l2',
                            min_df=3, max_df=0.95)
    def fit(self):
        tokenized_docs = (
                doc.to_terms_list(ngrams=1, named_entities=True, as_strings=True)
                for doc in self.corpus[:self.total_doc])
        self.doc_term_matrix = self.vectorizer.fit_transform(tokenized_docs)

    def transform(self, doc):
        tokenized_doc = doc.to_terms_list(
            ngrams=1, named_entities=True, as_strings=True)
        tfidf_doc = self.vectorizer.transform(tokenized_doc)

if __name__ == '__main__':
    wp = TextacyCorpusWikipedia(u'en')
    t = TfidfEmbeddingVectorizer(None, wp.corpus)
