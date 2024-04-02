#Brewery Db
Inhaltsverzeichnis
1. Projektübersicht
2. Daten
3. Prerequisites
4. Projekt-Verzeichnisübersicht
5. Kriterien
6. Docker Build & Azure Deployment
7 .Zukünftige Deployments

#Commands
```
#Activate Env
scripts/activate
#Start scraping:
cd src/load/scraper
scrapy crawl beer-spider -o ../../../res/data/raw_data.json -s CLOSESPIDER_PAGECOUNT=10
````
#Setup
###PyEnv
````
pyenv local 3.12.1
python -v -> 3.12.1
cd ..
python -m venv mdm_project1_brewerydb
````

https://www.zenrows.com/blog/scrapy-selenium#implement-selenium4-workaround
Setup eine file muss manuell in der scrapy-selenium library angepasst werden


#Docker Build


```
#Built local image
docker build -t dominikgsteiger/mdm-brewerydb .

# Testen, ob App funktional
docker run --name mdm-brewerydb -p 5000:5000 dominikgsteiger/mdm-brewerydb

docker push dominikgsteiger/mdm-brewerydb:latest


#Azure Cheatsheet
Wechseln von Subscription/abo auf Azure for Bildungseinrichtung war nötig
#Azure Login
az login

az group create --location switzerlandnorth --name mdm-brewerydb
az appservice plan create --resource-group mdm-brewerydb --name mdm-brewerydb --location switzerlandnorth
az webapp create --resource-group mdm-brewerydb --plan mdm-brewerydb --name mdm-brewerydb
az webapp config container set --resource-group mdm-brewerydb --name mdm-brewerydb --docker-custom-image-name dominikgsteiger/mdm-brewerydb:latest


 az container create --resource-group mdm-brewerydb --name mdm-brewerydb --image dominikgsteiger/mdm-brewerydb:latest --dns-name-label mdm-brewerydb --ports 5000
```

Link auf App:
http://mdm-brewerydb.switzerlandnorth.azurecontainer.io:5000/

| Kriterium | Bemerkung |
| -------- | -------- | 
| Datenquelle klar definiert   | | 
| Scraping vorhanden | |
| Scraping automatisiert | |
| Datensatz vorhanden  | |
| Erstellung Datensatz automatisiert, Verwendung Datenbank | |
| Datensatz-Grösse ausreichend, Aufteilung Train/Test, Kennzahlen vorhanden | |
| Modell vorhanden  | |
| Modell-Versionierung vorhanden (ModelOps) | |
| App: auf lokalem Rechner gestartet und funktional  | |
| App mehrere unterschiedliche Testcases durch Reviewer ausführbar  | |
| Deployment: Falls bereits vorhanden, funktional und automatisiert vorhanden  | |
| Code: Git-Repository vorhanden, Arbeiten mit Branches / Commits| |
| Code: Dependency Managment, Dockerfile, Build funktional  | |