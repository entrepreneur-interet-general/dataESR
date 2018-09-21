from selenium import webdriver
from scrapy.spiders import Spider
from campusfrance import CampusfranceItem
from scrapy import Request
from tqdm import tqdm
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.errorhandler import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from scrapy.settings.default_settings import LOG_FORMAT
import time

chromedriver = r'/home/sami/Documents/Chromedriver/chromedriver'

class CandidatureSpider(Spider):
    name = 'candidature'

    def __init__(self, *args, **kwargs):
        self.driver = webdriver.Chrome(executable_path=chromedriver)
        #self.driver = webdriver.Firefox()
        self.combinaisons = []
        self.last_position = 0
        self.items = []
        self.url = 'http://chercheurs.campusfrance.org/CandidatureAnonyme/recherche-externe'

        self.pbar = tqdm()  # initialize progress bar
        self.pbar.clear()
        self.pbar.write('Opening {} spider'.format(self.name))

    def start_requests(self):
        yield Request('http://chercheurs.campusfrance.org/CandidatureAnonyme/recherche-externe', self.parse)

    def parse_page_error(self, p):
        vide = "produit aucun".decode('utf8') \
                in self.driver.page_source
        non_vide = "ponse(s)".decode('utf8') \
                in self.driver.page_source
        trop_de_reponses = "veuillez affiner votre rechercher" \
                in self.driver.page_source
        erreur = "Erreur interne".decode('utf8') \
                in self.driver.page_source
        while erreur:
            self.reinitialize_driver()
            self.trigger_select(p)
            erreur = "Erreur interne".decode('utf8') \
                in self.driver.page_source
        if vide or trop_de_reponses:
            self.log('Page vide')
            self.reinitialize_driver()
            return None
        elif non_vide:
            self.log('Page non vide pour combinaison: %s' % p)
            return True
    
    def parse_select(self, elements):
        return [v.get_attribute('value') for v in elements[1:]]

    def parse_list_page(self, combinaison, multipays=False):
        all_results = self.driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div/div[4]/div/div/select')
        select = Select(all_results)
        select.select_by_value('100000')
        time.sleep(3)
        list_event = self.driver.find_elements_by_xpath(
            '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div/div[5]/div//a')
        size_elements = len(list_event)
        for i in range(size_elements):
            self.log(list_event)
            try:
                list_event[i].click()
            except StaleElementReferenceException:
                new_list_event = self.driver.find_elements_by_xpath(
                    '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div/div[5]/div//a')
                self.log("list event")
                self.log(new_list_event)
                self.driver.execute_script("arguments[0].scrollIntoView();", new_list_event[i])
                self.driver.execute_script("arguments[0].click()", new_list_event[i])
            if multipays:
                self.log('multipays')
                items = self.parse_page_multipays() 
                self.items = self.items + items
                for i in items:
                    yield i
            else:
                item = self.parse_page()
                self.items.append(item)
                yield item
            self.log('back driver')
            self.driver.back()
        self.reinitialize_driver()

    def parse_page(self):
        titre = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div[1]/div/div/h3').text
        annee_init = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div[3]/div/div/div[2]/span').text
        programme = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div/div/div[2]/span').text
        domaine = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div[4]/div/div/div[2]/span').text

        sigle = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/div/div/div[2]/span').text
        nom1 = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[3]/div/div/div/div/div[2]/div/div/div[2]/span').text
        adresse1 = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[3]/div/div/div/div/div[3]/div/div/div[2]/span').text
        cp1 = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[3]/div/div/div/div/div[4]/div/div/div[2]/span').text
        ville1 = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[3]/div/div/div/div/div[5]/div/div/div[2]/span').text
        institution_rattach1 = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[3]/div/div/div/div/div[6]/div/div/div[2]/span').text
        try:
            nom2 = self.driver.find_element_by_xpath(
                '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[4]/div/div/div/div/div[1]/div/div/div[2]/span').text
            adresse2 = self.driver.find_element_by_xpath(
                '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[4]/div/div/div/div/div[2]/div/div/div[2]/span').text
            cp2 = self.driver.find_element_by_xpath(
                '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[4]/div/div/div/div/div[3]/div/div/div[2]/span').text
            ville2 = self.driver.find_element_by_xpath(
                '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[4]/div/div/div/div/div[4]/div/div/div[2]/span').text
            pays2 = self.driver.find_element_by_xpath(
                '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[4]/div/div/div/div/div[5]/div/div/div[2]/span').text
            institution_rattach2 = self.driver.find_element_by_xpath(
                '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[4]/div/div/div/div/div[6]/div/div/div[2]/span').text
    
        except:
            nom2 = ""
            adresse2 = ""
            cp2 = ""
            ville2 = ""
            pays2 = ""
            institution_rattach2= ""

        item = CampusfranceItem(
            titre=titre,
            annee_init=annee_init,
            programme=programme,
            domaine=domaine,
            sigle=sigle,
            nom1=nom1,
            adresse1=adresse1,
            ville1=ville1,
            cp1=cp1,
            institution_rattach1=institution_rattach1,
            nom2=nom2,
            adresse2=adresse2,
            cp2=cp2,
            ville2=ville2,
            pays2=pays2,
            institution_rattach2=institution_rattach2
        )
        return item

    def parse_page_multipays(self):
        items = []
        self.log('Parsing multipays..')
        titre = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div[1]/div/div/h3').text
        self.log(titre)
        annee_init = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div[3]/div/div/div[2]/span').text
        programme = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div/div/div[2]/span').text
        domaine = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div[4]/div/div/div[2]/span').text

        sigle = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[3]/div/div/div/div/div[1]/div/div/div[2]/span').text
        nom1 = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[3]/div/div/div/div/div[2]/div/div/div[2]/span').text
        adresse1 = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[3]/div/div/div/div/div[3]/div/div/div[2]/span').text
        cp1 = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[3]/div/div/div/div/div[4]/div/div/div[2]/span').text
        ville1 = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[3]/div/div/div/div/div[5]/div/div/div[2]/span').text
        institution_rattach1 = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[3]/div/div/div/div/div[6]/div/div/div[2]/span').text
        n = len(self.driver.find_elements_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[4]/div/div/div'))
        for i in range(1, n+1):
            try:
                nom2 = self.driver.find_element_by_xpath(
                    '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[4]/div/div/div[{}]/div/div[1]/div/div/div[2]/span'.format(i)).text
                adresse2 = self.driver.find_element_by_xpath(
                    '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[4]/div/div/div[{}]/div/div[2]/div/div/div[2]/span'.format(i)).text
                cp2 = self.driver.find_element_by_xpath(
                    '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[4]/div/div/div[{}]/div/div[3]/div/div/div[2]/span'.format(i)).text
                ville2 = self.driver.find_element_by_xpath(
                    '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[4]/div/div/div[{}]/div/div[4]/div/div/div[2]/span'.format(i)).text
                pays2 = self.driver.find_element_by_xpath(
                    '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[4]/div/div/div[{}]/div/div[5]/div/div/div[2]/span'.format(i)).text
                institution_rattach2 = self.driver.find_element_by_xpath(
                    '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[4]/div/div/div[{}]/div/div[6]/div/div/div[2]/span'.format(i)).text
        
            except:
                nom2 = ""
                adresse2 = ""
                cp2 = ""
                ville2 = ""
                pays2 = ""
                institution_rattach2= ""

            item = CampusfranceItem(
                titre=titre,
                annee_init=annee_init,
                programme=programme,
                domaine=domaine,
                sigle=sigle,
                nom1=nom1,
                adresse1=adresse1,
                ville1=ville1,
                cp1=cp1,
                institution_rattach1=institution_rattach1,
                nom2=nom2,
                adresse2=adresse2,
                cp2=cp2,
                ville2=ville2,
                pays2=pays2,
                institution_rattach2=institution_rattach2
            )
            items.append(item)
        self.log('Total found items %s', len(items))
        return items

    # def construct_permutations(self, **kwargs):
    #     for i in kwargs['programme']:
    #         self.combinaisons.append(
    #          {
    #              'programme': i,
    #             }
    #         )
    #     self.log('Taille totale des permutations : %s' %
    #               len(self.combinaisons))

    def construct_permutations(self, **kwargs):
        for i in kwargs['programme']:
            for j in kwargs['domaine']:
                for y in kwargs['annee_init']:
                    self.combinaisons.append(
                       {
                           'programme': i,
                           'domaine': j,
                           'annee_init': y
                       }
                   )
        self.log('Taille totale des permutations : %s' %
                len(self.combinaisons))

    def parse(self, response):
        items = []
        self.driver.get(response.url)
        self.log('Starting to fill form')
        self.session_id = response.headers.getlist('Set-Cookie')[0]\
            .split(';')[0].split('=')[1]
        self.log('Cookies Session ID :%s' % self.session_id)
        self.log('Cookie selenium %s' % self.driver.get_cookies())

        programme = self.driver.find_element_by_xpath("//select[@id='id5']")
        domaine = self.driver.find_element_by_xpath("//select[@id='idf']")
        annee_init = self.driver.find_element_by_xpath("//select[@id='id8']")

        pprogramme = programme.find_elements_by_tag_name("option")
        pdomaine = domaine.find_elements_by_tag_name("option")
        pannee_init = annee_init.find_elements_by_tag_name("option")

        #les prog avec plus de 300 resultats et ceux qui restent
        #On calcule toutes les permutations seulement pour ceux qui
        #depassent les 300 resultats
        prog_300 = ['6', '9', '10', '40', '47'] 
        multi_pays = ['10007501', '48', '10007500', '10006500']
        self.log('Constructing permutations')
        self.construct_permutations(
            programme=prog_300,
            #programme=multi_pays,
            domaine=self.parse_select(pdomaine),
            annee_init=self.parse_select(pannee_init)
        )
        self.pbar.total = len(self.combinaisons)
        # debugging
        # self.combinaisons = [
        #     {
        #         'programme': u"10000351",
        #         #'domaine': u"38",
        #         #'annee_init': u"2010"
        #     }
        # ]
        #debut avec programme Maroc Toubkal
        for i, p in enumerate(self.combinaisons):
            self.log('-'*100)
            self.log(p)
            self.trigger_select(p)
            if self.parse_page_error(p):
                m = p['programme'] in multi_pays
                for item in self.parse_list_page(p, multipays=m):
                    yield item

            self.pbar.update(1)
        return

    def trigger_select(self, p):
        programme = self.driver.find_element_by_xpath(
            "//span[1]/div[2]/div/div/div[2]/select")
        domaine = self.driver.find_element_by_xpath(
            "//span[1]/div[6]/div/div/div[2]/select")
        annee_init = self.driver.find_element_by_xpath(
            "//span[1]/div[3]/div/div/div[2]/select")
        # annee_cours = self.driver.find_element_by_xpath(
        #     "//select[@id='idb']")

        select1 = Select(programme)
        select1.select_by_value(p['programme'])

        select2 = Select(domaine)
        select2.select_by_value(p['domaine'])
        select3 = Select(annee_init)
        select3.select_by_value(p['annee_init'])
        time.sleep(2)
        recherche = self.driver \
            .find_element_by_class_name("imageBoutonList")
        
        recherche.click()

    def reinitialize_driver(self):
        self.log('Closing current driver')
        self.log('Reinitializing driver')
        #self.driver.delete_all_cookies()
        self.driver.close()
        self.driver = webdriver.Chrome(executable_path=chromedriver)
        #self.driver = webdriver.Firefox()
        self.driver.get(self.url)
        self.log('Cookie selenium %s' % self.driver.get_cookies())

    def spider_closed(self, spider):
        self.driver.close()
        self.pbar.clear()
        self.pbar.write('Closing {} spider'.format(spider.name))
        self.pbar.close()  # close progress bar
