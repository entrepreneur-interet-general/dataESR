# Documentation du service Flask de tagging

Version supportée : `python 2.7`(`python 3.6`)

# Services

## Annotation avec une ontologie existante

2 modèles ont été entraîné permettant à un texte d'être annoter à partir d'une ontologie scientifique que repose soit sur celle du `scopus`, ou soit sur celle de la bibliothèque `PascalFrancis`.

### Scopus

### PascalFrancis

## Lier du texte à des entités Wikipedia


## Pour lancer le service

Pour lancer l'api :
```
sudo docker build -t tagger . 
sudo docker run -d -p 5000:5000 tagger
```

## Tester

```
cd tests
pytest
```