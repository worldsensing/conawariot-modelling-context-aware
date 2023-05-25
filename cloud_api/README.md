# Backend

## Setup

### Dependencies

If you plan running the backend locally (without Docker) or your idea is to run the tests:

Run `pip install -r requirements.txt` to install python dependencies.

### Create the Database

Execute the `setup_db.sh` file to set up the database tables.

## Run

After setup, run `make setup` and then `make start`.

## Tests

Just run `pytest`

----
To have the FastAPI backend running, a database has to be created in the PostgreSQL container,
to do so:

Open `localhost:5050`. The user and password are the ones that are shown in the `docker-compose.yml`.

To connect to the postgres database. Click in `Add New Server` and add the following information
in the `Connection` tab:

```bash
Host name/address: postgresdb
Port: 5432
Maintenance database: postgres
Username: postgres
Password: postgres
Role:
Service: