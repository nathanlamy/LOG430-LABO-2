#!/bin/sh

echo "Waiting for PostgreSQL to be ready..."

until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 2
done

echo "Postgres is up - running tests"
pytest