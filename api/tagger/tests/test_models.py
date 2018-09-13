import unittest
from textacy import Doc, Corpus
from models import TfidfEmbeddingVectorizer
import numpy as np
import os


class TestTfidfEmbeddingVectorizer(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(os.path.dirname(__file__), 'corpus_txt_test.txt'), 'rb') as f:
            texts = [t.decode('utf-8') for t in f.readlines()]
            self.corpus = Corpus(u'en', texts=texts)
        self.text = u"disease drop due economic disease else"
        self.doc = Doc(self.text)
        self.w2v = {w: 5 * np.random.random_sample((300,)) - 2 for w in self.text.split()}

    def test_tfidf_vectorizer(self):
        vectorizer = TfidfEmbeddingVectorizer(self.w2v, self.corpus)
        vectorizer.fit()
        tokenized_doc = [list(self.doc.to_terms_list(ngrams=1, named_entities=True, as_strings=True))]
        tfidf_doc = vectorizer.vectorizer.transform(tokenized_doc)
        v = tfidf_doc[:, vectorizer.vectorizer.vocabulary_terms['drop']].toarray()[0]
        doc_term_matrix = vectorizer.doc_term_matrix
        vectorizer.save(os.path.join(os.path.dirname(__file__), 'test_doc_term_matrix.npz'))
        vectorizer.load(os.path.join(os.path.dirname(__file__), 'test_doc_term_matrix.npz'), force=True)
        self.assertAlmostEqual(np.asscalar(v), 0.42063495, delta=0.05)
        self.assertEqual(vectorizer.transform(self.doc).shape, (300,))
        self.assertTrue(np.allclose(doc_term_matrix.toarray(), vectorizer.doc_term_matrix.toarray()))
