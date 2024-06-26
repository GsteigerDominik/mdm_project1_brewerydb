#Mdm Project 1 Brewery Db
Inhaltsverzeichnis:
1. Anforderungen 
2. Daten & Model Training
3. Architektur & CI / CD

##1. Anforderungen
| Kriterium | Bemerkung |
| -------- | -------- | 
| Datenquelle klar definiert|Siehe README 2.| 
| Scraping vorhanden | Code im Folder src/load/scraper, Daten im folder res/data |
| Scraping automatisiert | Code im Folder src/load/scraper, GitHubAction:  scrape_and_train |
| Datensatz vorhanden  | Siehe README 2.|
| Erstellung Datensatz automatisiert, Verwendung Datenbank | Code im Folder src/load/transform|
| Datensatz-Grösse ausreichend, Aufteilung Train/Test, Kennzahlen vorhanden |Siehe README 2. |
| Modell vorhanden  | Code im Folder src/load/model, Model im Folder res/model, Weiter Siehe README 2.|
| Modell-Versionierung vorhanden (ModelOps) | Siehe GitHubAction scrape_train, Siehe README 4. |
| App: auf lokalem Rechner gestartet und funktional  | Ausführen mit "python src/web/service.py"|
| App mehrere unterschiedliche Testcases durch Reviewer ausführbar  | Erreichbar unter http://127.0.0.1:5000|
| Deployment: Falls bereits vorhanden, funktional und automatisiert vorhanden  |GitHubAction: ci-cd |
| Code: Git-Repository vorhanden, Arbeiten mit Branches / Commits| https://github.com/GsteigerDominik/mdm_project1_brewerydb|
| Code: Dependency Managment, Dockerfile, Build funktional  | requirements.txt, Dockerfile, GitHubAction: ci-cd |
##2. Daten & Model Training
Die Daten werden von https://www.brewerydb.com bezogen. Es werden einzelne Biere oder Bierartige Getränke verwendet.
Der ABV-Wert(Alcohol by Volume) wiederspiegelt das numerische Target. 
Folgende Features sind vorhanden:
- Brew Style 
- SRM ( Standard Reference Method), Farbe von 1 (Ganz Hell z.B. Lager,) bis 40 (Ganz Dunkel z.B. Imperial Stout)
- Primary Flavor Notes, z.B. Sweet, Malt, Butterscotch, Caramel
- Serving Temperature, z.B. Cool - 8-12°C / 45-54°F 
- IBU (International Bitterness Unit) ca. 8-100

Folgende Features wurden mithilfe von Dummyvariablen vereinfacht:
- Brewstyle
- Primary Flavor Notes
- Serving Temperature

Mithilfe einer forward selection wurden folgende features ausgewählt:
- Bitterness (IBU), Numeric
- Cold (Serving Temperature), boolean
- American Style Imperial Stout (Brew Style), boolean
- Bittersweet, (Primary FLavor Notes), boolean
- Color (SRM), Numeric

Model: Lineare Regression:
- R2: ca 0.5
- Anzahl Datensätze: 416
- Anzahl Datensätze in guter Qualität: ca 350
- Anzahl Training: 70%
- Anzahl Validation: 30%


##3. Architektur & CI / CD
![ci-cd.png](ci-cd.png)
![scrape-train.png](scrape-train.png)
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
https://mdm-brewerydb.azurewebsites.net/
