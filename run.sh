#!/bin/bash

service nginx start

python manage.py migrate --noinput
python manage.py collectstatic --noinput

gunicorn -b 0.0.0.0:8001 echelon.wsgi
