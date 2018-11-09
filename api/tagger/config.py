import os
import logging

#FASTTEXT_FILE_MODEL_SCOPUS = os.path.join(os.getcwd(), 'data', 'model_scopus.bin')
#FASTTEXT_FILE_MODEL_PF = os.path.join(os.getcwd(), 'data', 'model_pf.bin')
#WIKIPEDIA2VEC_DIC_EN = os.path.join(os.getcwd(), 'data', 'wikipedia2vec_disambi_dic.pkl')
#WIKIPEDIA2VEC_MENTION_EN = os.path.join(os.getcwd(), 'data', 'wikipedia2vec_disambi_mention.pkl')

FASTTEXT_FILE_MODEL_SCOPUS = '/mnt/disk/wikipedia/bucket/model_scopus.bin'
FASTTEXT_FILE_MODEL_PF = '/mnt/disk/wikipedia/bucket/model_pf.bin'
WIKIPEDIA2VEC_DIC_EN = '/mnt/disk/wikipedia/model_wiki_dic.pkl'
WIKIPEDIA2VEC_MENTION_EN = '/mnt/disk/wikipedia/model_mention_0_1.pkl'

logging.basicConfig(
    filename=os.getenv('SERVICE_LOG', 'tagger.log'),
    level=logging.INFO,
    format='%(levelname)s: %(asctime)s module:%(module)s %(message)s',
    datefmt='%d/%m/%y %H:%M:%S',
)
