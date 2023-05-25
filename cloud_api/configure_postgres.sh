#!/usr/bin/env bash
DOCKER_POSTGRES=$1
DATABASE_NAME=$2

echo "Creating DATABASE $2 in container $1"
CREATE_DB="CREATE DATABASE $DATABASE_NAME"

sleep 3
if ! docker exec "$DOCKER_POSTGRES" psql -U postgres \
  -lqt | cut -d \| -f 1 | grep -q "$DATABASE_NAME"; then
  docker exec "$DOCKER_POSTGRES" psql -U postgres -c "$CREATE_DB"
  sleep 2
fi
