import os
import logging

### Using files names from model file in s3 bucket 
### https://s3.amazonaws.com/tagger-eig/models/models.tar.gz
FASTTEXT_FILE_MODEL_SCOPUS = os.path.join(
    os.getcwd(), 'data', 'model_scopus.bin')
FASTTEXT_FILE_MODEL_PF = os.path.join(
    os.getcwd(), 'data', 'model_pf.bin')
WIKIPEDIA2VEC_DIC_EN = os.path.join(
    os.getcwd(), 'data', 'wikipedia2vec_disambi_dic.pkl')
WIKIPEDIA2VEC_MENTION_EN = os.path.join(
    os.getcwd(), 'data', 'wikipedia2vec_disambi_mention.pkl')
WIKIPEDIA2VEC_DIC_FR = os.path.join(
    os.getcwd(), 'data', 'wikipedia2vec_fr_model_dic.pkl')
WIKIPEDIA2VEC_MENTION_FR = os.path.join(
    os.getcwd(), 'data', 'wikipedia2vec_fr_model_mention.pkl')

logging.basicConfig(
    filename=os.getenv('SERVICE_LOG', 'tagger.log'),
    level=logging.INFO,
    format='%(levelname)s: %(asctime)s module:%(module)s %(message)s',
    datefmt='%d/%m/%y %H:%M:%S',
)
