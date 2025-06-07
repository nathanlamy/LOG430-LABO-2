#!/bin/bash

docker compose down -v

docker compose build --no-cache

docker compose up -d db

# Try connecting for up to 20s
for i in {1..20}; do
  if docker exec log430-labo-2-db-1 pg_isready -U magasin_user > /dev/null 2>&1; then
    break
  fi
  echo "Waiting for DB ($i)..."
  sleep 1
done

echo "init DB"
docker compose run --rm -e DB_HOST=db -e DB_PORT=5432 -e DB_NAME=magasin -e DB_USER=magasin_user -e DB_PASSWORD=secret tests python init.py

echo "UI"
./run-client-web.sh 1
