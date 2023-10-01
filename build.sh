#!/bin/bash

# Installer les dépendances
pip install -r requirements.txt

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Effectuer les migrations de la base de données
python manage.py migrate

# Démarrer le serveur
gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT
