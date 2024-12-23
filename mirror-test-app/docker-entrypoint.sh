#!/bin/sh
if [ "$SQL_DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      echo "[x] Waiting PG service"
      sleep 0.1
    done

    echo "PostgreSQL started"

fi
poetry run alembic upgrade head

exec "$@"