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
