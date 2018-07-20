# coding:utf-8
from pymongo import MongoClient
from pywikibot.data import api, sparql
from pywikibot import pagegenerators as pg
from pprint import pprint
import pywikibot
import tqdm
import re


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


def read_file(path):
    with open(path, 'rb') as f:
        for l in f:
            yield l


def match_cnrs_to_wikidata(collection, doc):
    collection.insert_one(doc)


def sparkQL_query(site, query):
    return pg.WikidataSPARQLPageGenerator(query, site=site)


def get_info_from_id(repo, _id):
    item = pywikibot.ItemPage(repo, _id).get()
    if 'en' in item['labels'] and 'en' in item['descriptions']:
        return {'_id': _id, 'label': item['labels']['en'],
                'description': item['descriptions']['en']}
    else:
        return None


if __name__ == '__main__':
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    query = """
    SELECT ?item ?itemLabel
    WHERE
    {
    ?item wdt:%s wd:%s.
    SERVICE wikibase:label { bd:serviceParam wikibase:language
    "[AUTO_LANGUAGE],en". }
    }
    """
    dependencies = {'endpoint': None, 'entity_url': None}
    query_object = sparql.SparqlQuery(**dependencies)
    science = re.compile(r'(field|stud|academic|discipline|science)\
                           (y\b|ies\b|ied\b|\b|s\b)', re.IGNORECASE)
    subject = re.compile(r'.+?(?= \(|:|-)')
    infos = re.compile(r'\((.+?)(-|:)(.+?)\)')
    sc = re.compile(r'(.+?)( - | : )(.+)')
    connection = MongoClient('localhost', 27017)
    db = connection.CNRS
    coll = db.annuaire
    titres = [re.search(subject, x).group(0) for x in read_file('cnrs_annuaire')]
    print('Total titres: {}'.format(len(titres)))
    total = 0
    set_titre = set()
    for l in read_file('cnrs_annuaire'):
        titre = re.search(subject, l).group(0)
        if 'Sc.' in titre:
            titre = re.search(sc, l).group(3)
        set_titre.add(titre)
    for i in tqdm.tqdm(set_titre):
        search = get_items(site, i)['search']
        pprint(search)
        if len(search) > 0:
            desc = search[0].get('description')
            if desc is None:
                continue
            if science.search(desc):
                total += 1
                d = {
                    'id': search[0]['id'],
                    'description': search[0]['description'],
                    'label': search[0]['label'],
                    'titre': i
                }
                for prop in ['P527', 'P279', 'P361', 'P31']:
                    query_f = query % (prop, d['id'])
                    data = query_object.get_items(query_f,
                                                  item_name='item',
                                                  result_type=set)
                    if len(data) == 0:
                        continue
                    arr = []
                    for info_id in data:
                        arr.append(get_info_from_id(repo, info_id))
                    d.update({prop: arr})
                    print("Found for prop {} and label {}: {} elements"
                          .format(prop, d['label'], len(data)))
                coll.insert_one(d)
