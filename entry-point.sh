#!/bin/bash

service nginx start

sleep 10 # give other services time to spin up
python prod_manage.py collectstatic --noinput
python prod_manage.py migrate --noinput

gunicorn -b 0.0.0.0:8001 echelon.wsgi
