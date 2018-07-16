from pymongo import MongoClient
from pywikibot.data import api
import pywikibot
import tqdm
import re

# Login to wikidata
site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()

client = MongoClient('localhost', 27017)
db = client.wikidata
coll = db.science_test


r_en = re.compile(r'(field|stud|academic|discipline|science)(y\b|ies\b|ied\b|\b|s\b)', re.IGNORECASE)


def get_items(site, itemtitle):
    params = {'action': 'wbsearchentities', 'format': 'json',
              'language': 'fr', 'type': 'item', 'search': itemtitle}
    request = api.Request(site=site, **params)
    return request.submit()


def get_item(site, wdItem, token):
    request = api.Request(site=site,
                          action='wbgetentities',
                          format='json',
                          ids=wdItem)
    return request.submit()


def get_academic_entity(site, search):
    items = get_items(site, search)
    for item in items['search']:
        try:
            if r_en.search(item['description']):
                return item
        except:
            pass


def reinitialize_coll(coll, coll_test):
    for i in coll.find({}):
        coll_test.insert(i)


def get_id_from_properties(repo, entity_id, property_id='P31'):
    """yield Q id of the entity from the specific property"""
    claims = pywikibot.ItemPage(repo, entity_id).get()['claims']
    if property_id in claims:
        for item in claims[property_id]:
            yield {'id': item.getTarget().id, 'property': property_id}


def get_info_from_id(repo, _id):
    item = pywikibot.ItemPage(repo, _id).get()
    if 'en' in item['labels'] and 'en' in item['descriptions']:
        return {'_id': _id, 'label': item['labels']['en'],
                'description': item['descriptions']['en']}
    else:
        return None


def get_ids(coll):
    init_ids = []
    for i in coll.find({}, {'_id': 1}):
        init_ids.append(i['_id'])
    return init_ids


def add_element(repo, _id):
    item = pywikibot.ItemPage(repo, _id).get()
    if 'en' in item['labels'] and 'en' in item['descriptions']:
        record = {'label': item['labels']['en'], '_id': _id,
                  'description': item['descriptions']['en']}
        if not coll.count({'_id': _id}) > 0:
            coll.insert_one(record)


def add_element_from_properties(repo, _id, id_from_property, property_name):
    field = '.'.join(['family', property_name])
    info = get_info_from_id(repo, id_from_property)
    if info is None:
        return
    coll.update_one({'_id': _id}, {'$addToSet':
                    {field: {'id': id_from_property, 'label': info['label']}}},
                    upsert=True)
import pywikibot


def run_property(repo, property_id='P31'):
    for _id in tqdm.tqdm(get_ids(coll)):
        for el in get_id_from_properties(repo, _id, property_id=property_id):
            add_element(repo, el['id'])
            add_element_from_properties(repo, _id, el['id'], el['property'])

###################################################################
#                 Lecture de la nomenclature d'istex              #
###################################################################
# from pymongo import MongoClient

# client = MongoClient('localhost', 27017)
# db = client.istex
# springer = db.springer

# import tqdm
# scopus = set()
# wos = set()
# sciencemetrix = set()
# inist= set()
# for i in tqdm.tqdm(springer.find({'categories': {'$exists': True}, 'abstract': {'$exists': True}, 'title': {'$exists': True}, 'language': 'eng'})):
#             for ar, v in i['categories'].items():
#                 if ar == 'scopus':
#                     for el in v:
#                         scopus.add(el)
#                 if ar == 'wos':
#                     for el in v:
#                         wos.add(el)
#                 if ar == 'scienceMetrix':
#                     for el in v:
#                         sciencemetrix.add(el)
#                 if ar == 'inist':
#                     for el in v:
#                         inist.add(el)


if __name__ == '__main__':
    list_properties_to_check = ['P527', 'P279', 'P361', 'P31']
    for i in list_properties_to_check:
        run_property(repo, i)