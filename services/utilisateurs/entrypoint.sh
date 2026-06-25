#!/bin/sh
sleep 3
python manage.py migrate --noinput
exec "$@"
