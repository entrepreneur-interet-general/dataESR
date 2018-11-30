from textacy.datasets import Wikipedia
from textacy.io import split_records
from textacy import Vectorizer, Corpus
import io
import numpy as np
from scipy.sparse import save_npz, load_npz
import logging
import tqdm
import fastText
import celery
# from category import CategoryDatabase, CategoryTreeRobot
from wikipedia2vec import Wikipedia2Vec
from wikipedia2vec.dictionary import Dictionary
from wikipedia2vec.mention_db import MentionDB
from wikipedia2vec.utils.tokenizer.regexp_tokenizer import RegexpTokenizer

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s :: %(levelname)s :: %(message)s')

# class KnowledgeBase(object):
#     """
#     Build knowledge base from a dump.
#     catDB : - catContentDB: dict[category] = (subcatset, articleset)
#     """
#     def __init__(self, filename):
#         self.fn = filename
#         self.run()

#     def run(self):
#         catDB = CategoryDatabase(rebuild=False)
#         bot = CategoryTreeRobot('Scientific_disciplines', catDB, maxDepth=1)
#         bot.run()
#         ######
#         catDB = CategoryDatabase(rebuild=False, filename=self.fn)
#         catDB._load()
#         self.catDB = catDB

class TextacyCorpusWikipedia:
    def __init__(self, lang, filename, version='latest'):
        #super(KnowledgeBase, self).__init__(filename)
        self.lang = lang
        self.wp = Wikipedia(lang, version=version)
        self.wp.download()

    def build_corpus(self, size=-1):
        texts = self.wp.records(limit=size)
        text_stream, metadata_stream = split_records(texts, 'text')
        logging.info('building corpus...')
        self.corpus = Corpus(self.lang, texts=text_stream, metadatas=metadata_stream)


class TfidfEmbeddingVectorizer:
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
        for line in tqdm.tqdm(fin):
            tokens = line.rstrip().split(' ')
            data[tokens[0]] = map(float, tokens[1:])
        return data


class FastTextModel:
    def __init__(self, filename):
        logging.info('Loading fastText model {}'.format(filename))
        self.model = fastText.load_model(filename)
    def make_prediction(self, query, k, threshold):
        """
        - k (int):  Number of most likely classes returned (default: 1)
        - threshold (float): Filter classes with a probability below threshold (default: 0.0)
        """
        text = query['text']
        labels, probas = self.model.predict(text, k, threshold)
        return [{"label": l, "probas": p} for l, p in zip(labels, probas)]
    def build_context_vector(self, keywords):
        words = keywords.split()
        return self.model.get_sentence_vector(words)


class Wikipedia2VecModel:
    def __init__(self, lang, dic, mention_db):
        self.lang = lang
        self.dic = Dictionary.load(dic)
        self.mention_db = MentionDB.load(mention_db, self.dic)
    def detect_mentions(self, text):
        logging.info("Detecting mentions...")
        tokenizer = RegexpTokenizer()
        tokens = tokenizer.tokenize(text)
        response = []
        for mention in self.mention_db.detect_mentions(text, tokens):
            m = {
                "text": mention.text,
                "entity": mention.entity.title,
                "url": "https://{}.wikipedia.org/wiki/".format(self.lang) + \
                    mention.entity.title.replace(' ', '_')
            }
            if m not in response:
                response.append(m)
        return response


if __name__ == '__main__':
    wp = TextacyCorpusWikipedia(u'en')
    wp.build_corpus(size=10)
    w2v = TfidfEmbeddingVectorizer.load_vectors('wiki-news-300d-1M.vec')
    t = TfidfEmbeddingVectorizer(w2v, wp.corpus, total_doc=10)
    t.fit()
    t.save('10000_wiki.npz')
