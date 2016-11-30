#!/bin/bash

sleep 10 # give other services time to spin up
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py rebuild_index --noinput

gunicorn -b 0.0.0.0:8001 echelon.wsgi