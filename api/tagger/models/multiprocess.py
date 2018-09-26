
# coding: utf-8

# In[2]:


from gensim.corpora import MmCorpus


# In[36]:


from multiprocessing import Array, Process, Pool, Queue, Manager
import numpy as np
import tqdm
import sys
import gensim 
import numpy as np
import multiprocessing as mp

from gensim.models import TfidfModel
from gensim.corpora import Dictionary, MmCorpus

tf_idf_model = TfidfModel.load('/mnt/disk/wikipedia/wikipedia.tfidf_model')
dct = Dictionary.load_from_text('/mnt/disk/wikipedia/wikipedia_wordids.txt.bz2')
corpus = MmCorpus('/mnt/disk/wikipedia/wikipedia_bow.mm')

import io


# In[20]:


def load_vectors(fname):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    for line in tqdm.tqdm(fin):
        tokens = line.rstrip().split(' ')
        data[tokens[0]] = map(float, tokens[1:])
    return data

w2v_fasttext = load_vectors('wiki-news-300d-1M.vec')


# In[ ]:


import numpy as np

def map_w2v(w):
    if w in w2v_fasttext:
        return w2v_fasttext[w]
    else:
        return np.zeros(300)

def worker(ix, dictionary, corpus_wiki, tfidf_model):
    name = 'worker_{}_array'.format(ix)
    print(name, mp.current_process())
    init_stack = np.empty((0,300), float)
    for i, v in enumerate(corpus_wiki):
        if i % 6 == ix:
            words = map(lambda x: dictionary[x], [j[0] for j in v])
            w2v_corpus = map(map_w2v, words)
            tf_idf_weights = [x[1] for x in tf_idf_model[v]]
            mean_emb = np.mean([
                np.dot(tf_idf_weights[j], w2v_corpus[j]) for j in range(len(w2v_corpus))], axis=0)
            init_stack = np.vstack([init_stack, mean_emb])
        if i % 1000 == 0:
            print('saving ', i, ' th element', mp.current_process())
            np.save(name, init_stack)
            
processes = [mp.Process(target=worker, args = (i, dct, corpus, tf_idf_model)) for i in range(6)]

# Run processes
for p in processes:
    p.start()

# Exit the completed processes
for p in processes:
    p.join()

for p in processes:
    p.terminate()

