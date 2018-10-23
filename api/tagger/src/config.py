import os
import logging

#FASTTEXT_FILE_MODEL_SCOPUS = os.getenv('FASTTEXT_FILE_MODEL_SCOPUS')
FASTTEXT_FILE_MODEL_SCOPUS = '/Users/MACSAMI/Documents/Github/dataESR/api/tagger/models/model.bin'
FASTTEXT_FILE_VEC_FR = ''

URL_DATA = ''

logging.basicConfig(
    filename=os.getenv('SERVICE_LOG', 'tagger.log'),
    level=logging.INFO,
    format='%(levelname)s: %(asctime)s module:%(module)s %(message)s',
    datefmt='%d/%m/%y %H:%M:%S',
)
