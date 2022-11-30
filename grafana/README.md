# grafana

This component is Grafana, an open source tool (https://grafana.com/). 

Here we instantiate it using docker and docker-compose. One dashboard is configured to read 
information from the database, that contains the measurements of the system.

To run it, just execute `make setup` to run the dependencies (database) and then `make run` to 
run Grafana. Once done, to log in, credentials are located at the `./ENV/grafana.ini` file.