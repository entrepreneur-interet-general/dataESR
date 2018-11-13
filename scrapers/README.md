# Scrapy scrapers
## Installation
Si on utilise chrome pour selenium, ne pas oublier de télécharger le [chromedriver](http://chromedriver.chromium.org/downloads), et dans le cas de campusfrance, de mettre à jour le path (ligne 12).
## Créer un scraper
La librairie utilisée pour réaliser le scraping est [scrapy](https://scrapy.org/).

Pour lancer un nouveau projet, utilisez la commande : 
```
scrapy startproject [nom du projet]
```

## Lancer un scraper
Pour faire tourner un scraper :
```
cd (projet)
scrapy runspider (projet)/(projet)/spiders/***.py
```
## Documentation
L'ensemble de la documation `scrapy` est disponible [ici](https://docs.scrapy.org/en/latest/).

## Pour debugger
Un outil pratique pour débugger un site et regarder comment un spider réagit sur un site est le `shell` :
```
scrapy shell
```

## Scraping Campus France

Le scraping de ce site utilise `selenium`. Afin d'améliorer la vitesse de scraping, on différencie les programmes qui peuvent être scrapés en une requête et ceux qui nécessitent plusieurs requêtes car dépassant la limite de la recherche (cf la liste `prog_300` dans le fichier `candidature.py`).
