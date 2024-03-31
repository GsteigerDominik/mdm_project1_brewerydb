# Verwende ein offizielles Python-Laufzeit-Image als Basisimage
FROM python:3.12.1

# Setze das Arbeitsverzeichnis im Container
WORKDIR /usr/src/app

# Kopiere die aktuellen Verzeichnisinhalte in das Arbeitsverzeichnis im Container
COPY . .

# Installiere die benötigten Pakete
RUN pip install --no-cache-dir -r requirements.txt

# Mache Port 5000 für die Welt außerhalb dieses Containers verfügbar
EXPOSE 5000

# Führe app.py beim Start des Containers aus
CMD ["python", "src/web/service.py"]
