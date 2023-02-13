#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      echo $SQL_HOST
      echo $SQL_PORT
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate

exec "$@"