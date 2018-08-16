# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CampusfranceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    titre = scrapy.Field()
    annee_init = scrapy.Field()
    programme = scrapy.Field()
    domaine = scrapy.Field()
    sigle = scrapy.Field()
    nom1 = scrapy.Field()
    adresse1 = scrapy.Field()
    cp1 = scrapy.Field()
    ville1 = scrapy.Field()
    institution_rattach1 = scrapy.Field()
    nom2 = scrapy.Field()
    adresse2 = scrapy.Field()
    cp2 = scrapy.Field()
    ville2 = scrapy.Field()
    institution_rattach2 = scrapy.Field()
    pays2 = scrapy.Field()
