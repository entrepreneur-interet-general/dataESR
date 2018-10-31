# Documentation du service Flask de tagging

Version supportée : `python 2.7`(`python 3.6`)

# Services

## Extraire des mots clés

Le service permet d'extraire des mots clés d'un texte en utilisant la librairie `textacy` et en laissant le choix d'utiliser 3 types d'algorithmes non supervisés :
- [Textrank](https://chartbeat-labs.github.io/textacy/api_reference.html?highlight=keyterms#textacy.keyterms.sgrank)
- [SingleRank](https://chartbeat-labs.github.io/textacy/api_reference.html?highlight=keyterms#textacy.keyterms.sgrank)
- [SGRank](https://chartbeat-labs.github.io/textacy/api_reference.html?highlight=keyterms#textacy.keyterms.sgrank)

### API

#### POST /keywords

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

#### POST /predict_fasttext

### Scopus

### PascalFrancis

## Lier du texte à des entités Wikipedia

### API 

### POST /entity_linking

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