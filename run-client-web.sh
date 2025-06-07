# #!/bin/bash
docker build -t projet-caisse-web .

MAGASIN_ID=$1

if [ -z "$MAGASIN_ID" ]; then
  echo "Usage: ./run-client.sh <MAGASIN_ID>"
  exit 1
fi

docker run --rm -it \
  -e DB_HOST=10.194.32.204 \
  -e DB_PORT=5432 \
  -e DB_NAME=magasin \
  -e DB_USER=magasin_user \
  -e DB_PASSWORD=secret \
  -e MAGASIN_ID=$MAGASIN_ID \
  -p 5000:5000 \
  projet-caisse-web
