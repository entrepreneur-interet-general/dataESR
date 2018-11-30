# Documentation du service Flask de tagging

Version supportée : `python 3.6`
Docker version testée : `Docker version 18.06.1-ce, build e68fc7a`

❗️ La version dockerisé nécessite au moins 15go par défault pour que le container puisse se lancer.

# Services

## Pour lancer le service

Pour lancer l'api :
```
sudo docker build -t tagger . 
sudo docker run -d -p 5000:5000 tagger
```

## Infos

Le service utilise un bucket `s3` pour télécharger les modèles construits à l'adresse suivante : `https://s3.amazonaws.com/tagger-eig/models/models.tar.gz`.
Si ce fichier change, il faut mettre à jour dans le fichier `config.py` les nouveaux noms correspondant aux modèles et le `Dockerfile`.

## Extraire des mots clés

Le service permet d'extraire des mots clés d'un texte en utilisant la librairie `textacy` et en laissant le choix d'utiliser 3 types d'algorithmes non supervisés :
- [Textrank](https://chartbeat-labs.github.io/textacy/api_reference.html?highlight=keyterms#textacy.keyterms.sgrank)
- [SingleRank](https://chartbeat-labs.github.io/textacy/api_reference.html?highlight=keyterms#textacy.keyterms.sgrank)
- [SGRank](https://chartbeat-labs.github.io/textacy/api_reference.html?highlight=keyterms#textacy.keyterms.sgrank)

### API

#### POST /tagger/keywords

#### Example request

```json
{
    "text": "Coherent coupling of individual quantum dots measured with phase-referenced two-dimensional spectroscopy: Photon echo versus double quantum coherence",
    "params": {
        "normalize": null
    },
    "method": "sgrank"
}
```
| Name | Type | Description |
| ---- | ---- | ----------- |
| `text` | string | Text to be processed |
| `method` | string | Method to use to extract text (default: `sgrank`)|
| `params` | dict | Parameters to use with the methods if not default ones | 

#### Example response :
```json
{
    "keywords": [
        [
            "double quantum coherence",
            0.332025205
        ],
        [
            "individual quantum dots",
            0.2871810581
        ],
        [
            "Coherent coupling",
            0.136428876
        ],
        [
            "dimensional spectroscopy",
            0.0986504819
        ],
        [
            "Photon",
            0.0736771638
        ],
        [
            "phase",
            0.0720372152
        ]
    ]
}
```

## Annotation avec une ontologie existante

2 modèles ont été entraîné permettant à un texte d'être annoter à partir d'une ontologie scientifique que repose soit sur celle du `scopus`, ou soit sur celle de la bibliothèque `PascalFrancis`.

### API

#### POST /tagger/predictions_fasttext

### Scopus

#### entrainement

L'entrainement de ce modèle repose sur les données de la base *ISTEX* en utilisant comme annotation l'ontologie de la base SCOPUS et utilise la librairie `fastText` de Facebook.

#### Example request :
```json
{
    "text": "Coherent coupling of individual quantum dots measured with phase-referenced two-dimensional spectroscopy: Photon echo versus double quantum coherence",
    "model": "scopus",
    "k": 3
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `text` | string | Text to be processed |
| `model` | string | Model to use ("scopus") |
| `k` | int | Number of predictions to display (default: 1) |
| `threshold`| float | Fasttext threshold (default: 0) |

#### Exemple response :

```json
{
  "labels": [
    {
      "label": "Physics and Astronomy",
      "probas": 0.37525737285614014
    },
    {
      "label": "General Physics and Astronomy",
      "probas": 0.23475822806358337
    },
    {
      "label": "Physical Sciences",
      "probas": 0.20027048885822296
    }
  ]
}
```
### PascalFrancis

#### entrainement

L'entrainement de ce modèle repose sur les données de la base *PascalFrancis* en utilisant son ontologie comme annotation et la librairie `fastText` de Facebook.

#### Example request :
```json
{
    "text": "Coherent coupling of individual quantum dots measured with phase-referenced two-dimensional spectroscopy: Photon echo versus double quantum coherence",
    "model": "pf",
    "k": 3
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `text` | string | Text to be processed |
| `model` | string | Model to use ("scopus") |
| `k` | int | Number of predictions to display (default: 1) |
| `threshold`| float | Fasttext threshold (default: 0) |

#### Example response :
```json
{
  "labels": [
    {
      "label": "pascal::001B::fr Physique::en Physics",
      "probas": 0.15214012563228607
    },
    {
      "label": "pascal::001::fr Sciences exactes et technologie::en Exact sciences and technology",
      "probas": 0.07756912708282471
    },
    {
      "label": "macrodomain::pec::fr Physique de l'\u00e9tat condens\u00e9::en Condensed state physics",
      "probas": 0.0654236301779747
    }
  ]
}
```
## Lier du texte à des entités Wikipedia

Ce service permet d'extraire du texte des entités existant dans Wikipedia en utilisant un framework open source appelé [Wikipedia2vec](https://wikipedia2vec.github.io).

### API 

#### POST /tagger/entity_linking

#### Example request :
```json
{
    "text": "Coherent coupling of individual quantum dots measured with phase-referenced two-dimensional spectroscopy: Photon echo versus double quantum coherence"
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `text` | string | Text to be processed |

#### Example response :
```json
[
    {
        "entity": "Quantum dot",
        "text": "quantum dots",
        "url": "https://en.wikipedia.org/wiki/Quantum_dot"
    },
    {
        "entity": "Photon",
        "text": "Photon",
        "url": "https://en.wikipedia.org/wiki/Photon"
    },
    {
        "entity": "Coherence (physics)",
        "text": "quantum coherence",
        "url": "https://en.wikipedia.org/wiki/Coherence_(physics)"
    }
]
```
| Name | Type | Description |
| ---- | ---- | ----------- |
| `entity` | string | Wikipedia entity |
| `text` | string | Text linked to the entity |
| `url` | string | Wikipedia url of the entity |


## Tester

```
cd tests
pytest
```