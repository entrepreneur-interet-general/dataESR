from textacy.datasets import Wikipedia
from textacy.io import split_records
from textacy import Vectorizer, Corpus
import io
import numpy as np
from scipy.sparse import save_npz, load_npz
import logging
import tqdm

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s :: %(levelname)s :: %(message)s')

class TextacyCorpusWikipedia(object):
    def __init__(self, lang, version='latest'):
        self.lang = lang
        self.wp = Wikipedia(lang, version=version)
        self.wp.download()

    def build_corpus(self, size=-1):
        texts = self.wp.records(limit=size)
        text_stream, metadata_stream = split_records(texts, 'text')
        logging.info('building corpus...')
        self.corpus = Corpus(self.lang, texts=text_stream, metadatas=metadata_stream)


class TfidfEmbeddingVectorizer(object):
    """
    Building tfidf weighted scheme out of a textacy Corpus.
    """
    def __init__(self, w2v, corpus, dim=300, total_doc=100):
        self.dim = dim
        self.w2v = w2v
        self.corpus = corpus
        self.total_doc = total_doc
        self.vectorizer = Vectorizer(
                            apply_idf=True, norm='l2',
                            min_df=3, max_df=0.95)
        self.doc_term_matrix = None

    def fit(self):
        logging.info('Fitting vectorizer with corpus...')
        tokenized_docs = (
                doc.to_terms_list(ngrams=1, named_entities=True, as_strings=True)
                for doc in tqdm.tqdm(self.corpus[:self.total_doc]))
        self.doc_term_matrix = self.vectorizer.fit_transform(tokenized_docs)

    def transform(self, doc):
        tokenized_doc = [doc.to_terms_list(
            ngrams=1, named_entities=True, as_strings=True)]
        tfidf_doc = self.vectorizer.transform(tokenized_doc)
        return np.array([
            np.mean([self.w2v[w] * tfidf_doc[:, self.vectorizer.vocabulary_terms[w]].toarray()[0]
                     for w in tokenized_doc[0] if w in self.corpus.spacy_vocab] or
                    [np.zeros(self.dim)], axis=0)
        ]).flatten()
    
    def save(self, filename):
        logging.info('Saving doc term matrix in filename: %s', filename)
        if self.doc_term_matrix is None:
            raise Exception('Nothing to save.')
        else:
            save_npz(filename, self.doc_term_matrix)
    
    def load(self, filename, force=False):
        if self.doc_term_matrix is not None:
            if not force:
                logging.error('tf-idf matrix not empty, set force=True to overwrite.')
                raise Exception('tf-idf matrix not empty, set force=True to overwrite.')
        logging.info('Loading doc term matrix from filename: ', filename)
        self.doc_term_matrix = load_npz(filename)

    @staticmethod
    def load_vectors(fname):
        logging.info('Reading vectors from file: %s', fname)
        fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
        n, d = map(int, fin.readline().split())
        data = {}
        for line in fin:
            tokens = line.rstrip().split(' ')
            data[tokens[0]] = map(float, tokens[1:])
        return data


if __name__ == '__main__':
    wp = TextacyCorpusWikipedia(u'en')
    wp.build_corpus(size=10)
    w2v = TfidfEmbeddingVectorizer.load_vectors('wiki-news-300d-1M.vec')
    t = TfidfEmbeddingVectorizer(w2v, wp.corpus, total_doc=10)
    t.fit()
    t.save('10000_wiki.npz')
