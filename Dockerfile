# Basis-Image
FROM python:3.11-slim

# Arbeitsverzeichnis setzen
WORKDIR /app

# Dateien kopieren
COPY . .

# Abhängigkeiten installieren
RUN pip install --no-cache-dir -r requirements.txt

# Upload-Ordner erstellen
RUN mkdir -p static/uploads

# Port für Render/Cloud öffnen
ENV PORT=8080
EXPOSE 8080

# Startbefehl
CMD ["python", "app.py"]
