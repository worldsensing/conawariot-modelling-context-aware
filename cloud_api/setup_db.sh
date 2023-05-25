# WARNING: Script for testing and debugging purposes
docker compose -f docker-compose.yml stop postgres pgadmin
sudo rm -rf /var/opt/api_modelling_local/pg_data

# Initialize the backend
docker compose -f docker-compose.yml up -d --force-recreate --no-deps postgres
sh ./configure_postgres.sh cloud_api-postgres-1 apidb
docker compose -f docker-compose.yml stop postgres