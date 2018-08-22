Version supportée : `python 2.7`

# Lancer
Pour lancer l'api :
```
sudo docker build -t tagger . 
sudo docker run -d -p 5000:5000 tagger
```

# Tester

```
cd tests
pytest
```