import random
from datetime import datetime, timezone
from time import sleep

import requests

SERVERS = {
    "local": "http://localhost:5001",
    "deploy": "http://localhost:8000/api"
}
SEL_SERVER = "deploy"

DEVICE = {
    "name": "ABC-1001",
    "type": "Inclinometer"
}
SEL_THING = DEVICE

OBSERVATION = {
    "device_name": SEL_THING["name"],
    "value": "AUTOMATICALLY_GATHERED",
    "time_start": "AUTOMATICALLY_GATHERED"
}
SEL_OBSERVATION = OBSERVATION


# Format: 2020-03-24T14:17:12Z
def get_current_date_time():
    now = datetime.now(timezone.utc)
    # now = now - timedelta(minutes=29)
    now = now.replace(microsecond=0)

    return now.isoformat()


def post_info(url, body):
    response = requests.post(url, json=body)
    print(response)


def add_thing(thing):
    url = f"{SERVERS[SEL_SERVER]}/things"
    print(f"Adding Thing to {url}")
    print(thing)

    post_info(url, thing)


def add_observation(observation):
    url = f"{SERVERS[SEL_SERVER]}/observations"
    print(f"Adding Observation to {url}")

    # Generates a value from an uniform 0 1, and round it to 4 decimals
    observation["value"] = str(round(random.uniform(0, 1), 4))
    observation["time_start"] = get_current_date_time()

    print(observation)

    post_info(url, observation)


if __name__ == "__main__":
    add_thing(SEL_THING)
    while True:
        add_observation(SEL_OBSERVATION)
        sleep(2)
