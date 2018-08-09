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
