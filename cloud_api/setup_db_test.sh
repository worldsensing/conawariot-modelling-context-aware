# Script just for testing and debugging purposes
docker-compose -f docker-compose.test.yml -p phd_deployment_test stop
sudo rm -rf /var/opt/api_modelling_test/pg_data

docker-compose -f docker-compose.test.yml -p phd_deployment_test up -d postgres
sh ./scripts/configure_postgres.sh phd_deployment_test_postgres_1 api_db_test
docker-compose -f docker-compose.test.yml -p phd_deployment_test stop
