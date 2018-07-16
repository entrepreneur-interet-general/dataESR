#coding:utf-8
import scrapy
from ids_gican import URLS_GICAN
from gifas import GicanItem
import sys  
import re 

class Gican(scrapy.Spider):
    name = 'gican'

    def start_requests(self):
        for url in URLS_GICAN:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        name = response.xpath('//*[@id="rsoc"]/text()').extract_first()
        resume = response.xpath('/html/body/div[3]/div[1]/div[2]/text()').extract_first()
        logo = response.xpath('/html/body/div[3]/div[2]/img/@src').extract_first()
        adresse = response.xpath('/html/body/div[3]/div[2]/text()').extract()
        dirigeants = response.xpath('/html/body/div[3]/div[2]/text()').extract()
        nomenclature = response.xpath('/html/body/div[3]//ul//li/text()').extract()
        site = response.xpath('/html/body/div[3]/div[2]/a[1]/text()').extract_first()
        contact = response.xpath('/html/body/div[3]/div[2]/a[2]/text()').extract_first()
        # self.log(nomenclature)
        # self.log(self.get_ix_nomenclature(nomenclature))
        entreprise = GicanItem(
            name = name,
            resume = self.clean_tag(resume),
            logo = 'http://j2c-com.com/gican17/enligne/' + logo,
            adresse = self.clean_tag(';'.join(adresse)),
            dirigeants =  self.clean_tag(';'.join(dirigeants)),
            nomenclature = ';'.join(nomenclature),
            site = site,
            contact = contact
        )
        return entreprise

    def clean_tag(self, text):
        return re.sub('<[^<]+?>', '', text) \
                    .replace('\n', '') \
                    .replace(u'\xa0', '') \
                    .strip()

    def get_ix_nomenclature(self, selectors):
        for i, s in enumerate(selectors):
            if 'Nomenclature' in s.xpath('/text()').extract_first():
                return i