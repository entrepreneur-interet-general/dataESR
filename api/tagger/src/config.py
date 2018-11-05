import os
import logging

#FASTTEXT_FILE_MODEL_SCOPUS = os.getenv('FASTTEXT_FILE_MODEL_SCOPUS')
FASTTEXT_FILE_MODEL_SCOPUS = '/Users/MACSAMI/Documents/Github/dataESR/api/tagger/models/model.bin'
FASTTEXT_FILE_VEC_FR = ''
WIKIPEDIA2VEC_DIC_EN = '/Users/MACSAMI/Documents/Github/dataESR/api/tagger/models/wikipedia2vec_disambi_dic.pkl'
WIKIPEDIA2VEC_MENTION_EN = '/Users/MACSAMI/Documents/Github/dataESR/api/tagger/models/wikipedia2vec_disambi_mention.pkl'
WIKIPEDIA2VEC_EMBEDDINGS_EN = '/Users/MACSAMI/Documents/Github/dataESR/api/tagger/models/wikipedia2vec_embeddings'


logging.basicConfig(
    filename=os.getenv('SERVICE_LOG', 'tagger.log'),
    level=logging.INFO,
    format='%(levelname)s: %(asctime)s module:%(module)s %(message)s',
    datefmt='%d/%m/%y %H:%M:%S',
)
