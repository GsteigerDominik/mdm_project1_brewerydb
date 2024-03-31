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
docker build -t mdm-brewerydb .

# Testen, ob App funktional
docker run --name mdm-brewerydb -p 5000:5000 mdm-brewerydb
```