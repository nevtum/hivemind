#!/bin/bash

service nginx start

python prod_manage.py migrate --noinput
python prod_manage.py collectstatic --noinput

gunicorn -b 0.0.0.0:8001 echelon.wsgi
