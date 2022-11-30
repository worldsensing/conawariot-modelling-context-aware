# Script just for testing and debugging purposes
docker-compose -f docker-compose.yml -p phd_deployment stop
sudo rm -rf /var/opt/api_modelling_local/pg_data

docker-compose -f docker-compose.yml -p phd_deployment up -d postgres
sh ./scripts/configure_postgres.sh phd_deployment_postgres_1 api_db
docker-compose -f docker-compose.yml -p phd_deployment stop
