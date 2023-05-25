import json

import requests

import utils
from __init__ import URL_ONTOLOGY_DEPLOYMENT_LOCAL, ONTOLOGY_SENSOR_NAME, ONTOLOGY_OBSERVABLE_PROPERTY

BASE_URL = URL_ONTOLOGY_DEPLOYMENT_LOCAL
SENSORS_ENDPOINT_URL = "/sensors/"
SENSOR_OBSERVATIONS_ENDPOINT_URL = "/observations/"  # TODO Change to /sensor-observations/
OBSERVATIONS_ENDPOINT_URL = "/observations/"
OBSERVABLE_PROPERTIES_ENDPOINT_URL = "/observable-properties/"


def post_sensor_observation(value, sensor_name=ONTOLOGY_SENSOR_NAME,
                            observable_property=ONTOLOGY_OBSERVABLE_PROPERTY):
    print(f"Sending POST to create an observation")
    url = f"{BASE_URL}{OBSERVATIONS_ENDPOINT_URL}"
    print(url)
    body = {"sensor_name": sensor_name, "observable_property": observable_property,
            "time_start": utils.get_current_time(), "value_int": value}
    print(body)

    r = requests.post(url, json=body)
    try:
        observation = json.loads(r.content)
        print(observation)

        return observation["id"]
    except:
        pass

    return None