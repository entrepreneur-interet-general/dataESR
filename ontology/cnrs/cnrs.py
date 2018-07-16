# coding:utf-8
from pymongo import MongoClient
from pywikibot.data import api
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


if __name__ == '__main__':
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()

    subject = re.compile(r'.+?(?= \(|:|-)')
    infos = re.compile(r'\((.+?)(-|:)(.+?)\)')
    sc = re.compile(r'(.+?)( - | : )(.+)')
    connection = MongoClient('localhost', 27017)
    db = connection.CNRS
    coll = db.annuaire
    titres = [re.search(subject, x).group(0) for x in read_file('cnrs_annuaire')]
    print('Total titres: {}'.format(len(titres)))
    total = 0
    for l in read_file('cnrs_annuaire'):
        titre = re.search(subject, l).group(0)
        if 'Sc.' in titre:
            titre = re.search(sc, l).group(3)
        coll.insert_one({'terme': titre})

