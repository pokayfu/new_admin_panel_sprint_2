#!/bin/sh

cd data_to_db && python main.py && cd ..

python manage.py collectstatic --no-input

python manage.py migrate

python manage.py compilemessages -l en -l ru 

python manage.py createsuperuser --noinput || true

uwsgi --strict  --ini  uwsgi.ini
