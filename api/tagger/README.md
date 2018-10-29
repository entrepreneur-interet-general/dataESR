# Documentation du service Flask de tagging

Version supportée : `python 2.7`(`python 3.6`)

# Services

## Annotation avec une ontologie existante

2 modèles ont été entraîné permettant à un texte d'être annoter à partir d'une ontologie scientifique que repose soit sur celle du `scopus`, ou soit sur celle de la bibliothèque `PascalFrancis`.

### API

#### POST /predict_fasttext

### Scopus

### PascalFrancis

## Lier du texte à des entités Wikipedia

### POST /entity_linking

#### Example request :
```json
{
    "text": "Coherent coupling of individual quantum dots measured with phase-referenced two-dimensional spectroscopy: Photon echo versus double quantum coherence"
}
```

| Name | Type | Description |
| ---- | ---- | ----------- |
| `text` | string | Text to be processsed |

#### Example response
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