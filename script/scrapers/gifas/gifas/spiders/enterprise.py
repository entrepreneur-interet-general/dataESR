import scrapy
from gifas import GifasItem
from scrapy.loader import ItemLoader
import re
import sys  

url = 'https://www.gifas.asso.fr/node/'
path_file = '/home/sami/Documents/Workplace/gifas.txt'


class Entreprise(scrapy.Spider):
    name = 'entreprises'
    def start_requests(self):
        with open(path_file, 'rb') as f:
            lines = f.readlines()
            tuple_l = map(lambda x: x.split(', '),lines)
            urls = map(lambda x: x[1].replace('\n', ''), tuple_l)
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        name = response.css('div#FicheAnnuaire table tbody tr td h1::text').extract_first()
        adresse = response.css('div#FicheAnnuaire table tbody tr td#FicheAnnuaireAdresse p').extract_first().replace(u'&nbsp;', '').split('<br>')
        adresse = '/'.join(map(lambda x: x.strip(), adresse))
        logo = response.css('div#FicheAnnuaire table tbody tr td img::attr(src)').extract_first()
        dirigeants = len(response.xpath('//*[@id="FicheAnnuaire"]/table[3]/tbody/tr/td/table'))

        l_dir = []
        for s in range(dirigeants):
            s += 1
            poste = response.xpath('//*[@id="FicheAnnuaire"]/table[3]/tbody/tr/td/table[{}]/tbody/tr/td[1]/text()'.format(s)).extract_first().replace('\n','').replace(u'\xa0','').strip()
            n = response.xpath('//*[@id="FicheAnnuaire"]/table[3]/tbody/tr/td/table[{}]/tbody/tr/td[3]/text()'.format(s)).extract_first().replace('\n','').split(u'\xa0')
            n = ' '.join(map(lambda x: x.strip(), n))
            l_dir.append((poste, n))
        l_dir = ','.join(map(lambda x : self.clean_tag(x[0] +':'+x[1]), l_dir))

        activites = response.css('div#FicheAnnuaire table#activites.showContent tbody tr td p:nth-of-type(4)').extract_first().replace('<br>', '')
        ixactivite = response.css('#produits > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr')
        
        groupe = response.css('div#FicheAnnuaire table tbody tr td p b::text').extract_first()
        
        size = len(response.xpath('//*[@id="produits"]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr'))
        ix = []
        for i in range(size):
            i += 1
            path = '//*[@id="produits"]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[' + str(i) + ']/td/text()'
            ix.append(response.xpath(path).extract_first().replace('\n', '').strip())

        entreprise = GifasItem( 
            name = name,
            adresse = self.clean_tag(adresse).replace('\n', '').strip(),
            logo =  'https://www.gifas.asso.fr' + logo,
            dirigeants = l_dir,
            activites = self.clean_tag(activites),
            groupe = groupe,
            ixactivites = '/'.join(ix),
            site = response.url
        )

        self.log('Visited company %s' % name)
        return entreprise

    def clean_tag(self, text):
        return re.sub('<[^<]+?>', '', text) \
                    .replace('\n', '') \
                    .replace(u'\xa0', '') \
                    .strip()