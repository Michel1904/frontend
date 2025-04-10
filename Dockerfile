FROM python:3.12

WORKDIR /app

# Copier tous les fichiers dans /app
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir -r streamlit_requirements.txt

# Lancer l'application Streamlit
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=80", "--server.enableCORS=false"]
