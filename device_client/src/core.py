import json

import requests

import utils
from __init__ import URL_ONTOLOGY_DEPLOYMENT_LOCAL, ONTOLOGY_SENSOR_NAME

BASE_URL = URL_ONTOLOGY_DEPLOYMENT_LOCAL
CONTEXT_AWARENESS_ENDPOINT_URL = "/context-aware-rules/"
SENSORS_ENDPOINT_URL = "/sensors/"
SENSOR_OBSERVATIONS_ENDPOINT_URL = "/observations/"  # TODO Change to /sensor-observations/
OBSERVATIONS_ENDPOINT_URL = "/observations/"
OBSERVABLE_PROPERTIES_ENDPOINT_URL = "/observable-properties/"
ACTUATIONS_ENDPOINT_URL = "/actuations/"


def post_sensor_observation(value, sensor_name=ONTOLOGY_SENSOR_NAME):
    print(f"Sending POST to create an observation")
    url = f"{BASE_URL}{OBSERVATIONS_ENDPOINT_URL}"
    print(url)
    body = {"sensor_name": sensor_name, "time_start": utils.get_current_time(), "value": value}
    print(body)

    r = requests.post(url, json=body)
    observation = json.loads(r.content)["data"]
    print(observation)

    return observation["id"]
