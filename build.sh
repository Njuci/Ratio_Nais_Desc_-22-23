#!/bin/bash

# Installer les dépendances
pip install -r requirements.txt

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Effectuer les migrations de la base de données
python manage.py migrate

# Démarrer le serveur
gunicorn ratio_nais_desc.wsgi:application --bind 0.0.0.0:$PORT
