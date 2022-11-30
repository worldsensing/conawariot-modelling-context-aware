# cloud_api

This project contains a `Python Flask` API and also a `PostreSQL` database. Run using `Docker`.

A `Swagger` file and a `jsonschema` file are also provided for this project, in this same folder.

## Requirements

- Docker
- Docker-compose

## Setup & Usage

### Run project

Execute in terminal

- `sh setup_db.sh`
- `make run`

Code is then available at `http:\\localhost:5001`.

### Run tests

Execute in terminal:

- `sh setup_db_test.sh`
- `make setup-tests`
- `make run-tests`
