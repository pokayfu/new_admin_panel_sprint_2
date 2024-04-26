#!/bin/sh

psql -h 127.0.0.1 -U app -d movies_database -f ./data_to_db/movies_database.ddl 

python manage.py migrate

cd data_to_db && python main.py && cd ..

uwsgi --ini uwsgi.ini