#!/bin/sh

cd data_to_db && python main.py && cd ..

python manage.py migrate

uwsgi --ini uwsgi.ini