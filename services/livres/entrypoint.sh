#!/bin/sh
echo "En attente de PostgreSQL..."
sleep 3

echo "Application des migrations..."
python manage.py migrate --noinput

echo "Démarrage du serveur..."
exec "$@"
