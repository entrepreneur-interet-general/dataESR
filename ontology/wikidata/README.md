## Construction du graphe wikipedia

Source : `category.py`

Pour lancer le parsing des category :
```python
catDB = CategoryDatabase(rebuild=True, filename='nom_du_fichier_ou_dump')
bot = CategoryTreeRobot('Computer_science', catDB, maxDepth=1)
bot.run()
````
Ensuite, dump dans un fichier le dictionnaire des relations qui a été construit.

```python
catDB.dump()
```
Ensuite on peut construire dans `neo4j` le graphe :

```python
catDB.dump_neo(host='localhost', user='user', password='admin')
```

##  Quelques requêtes intéressantes

* Pour une catégorie comme *Fiscal policy* :

Avoir toutes les catégories qui proviennent de la même categorie parente

```cypher
MATCH (:Categorie{name:"Fiscal policy"})<-[:HAS_SUBCLASS*0..]-(:Categorie)-[:HAS_SUBCLASS*0..1]->(cat:Categorie)
RETURN cat
```

## Pickles

Pour charger un fichier pickle spécifique :
```
catDB = CatagoryDatabase(filename='fichier_pickle')
catDB._load()
```
Cela donne accès directement aux bases enregistrées :
- superclassDB
- catContentDB

`catContentDB` correspond à un dictionnaire où la clé est un object `Category` *X* et la valeur un tuple de `set` où le premier élément et l'ensemble des sous catégorie, et le second les articles qui ont cette catégorie *X*.