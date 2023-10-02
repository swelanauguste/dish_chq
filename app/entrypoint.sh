#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# python manage.py migrate 

# python manage.py makemigrations
# python manage.py migrate

# python manage.py createsuperuser --username kingship --email kingship.lc@gmail.com --noinput

# python manage.py add_returns
# python manage.py add_cheque_status
# python manage.py add_ministries
# python manage.py add_owners
# python manage.py add_cheques

# python manage.py migrate --run-syncdb

python manage.py collectstatic --noinput

exec "$@"