import json
from typing import List

import requests

from src import BASE_URL, API_SENSORS_ENDPOINT, API_SENSOR_OBSERVATIONS_ENDPOINT, \
    API_ACTUATOR_ENDPOINT, API_ACTUATION_ENDPOINT, actuators, core, utils, \
    API_PROCEDURE_TYPE_NAME_ENDPOINT


def check_event_rule(event_rule: dict) -> bool:
    er_type_obj = core.get_event_rule_type(event_rule["event_rule_type_name"])

    er_type = er_type_obj["event_rule_type"]
    er_comparation_type = er_type_obj["event_rule_comparation_type"]
    er_value_type = er_type_obj["event_rule_value_type"]

    sensor_1_data = core.get_last_observation_from_sensor_name(er_value_type,
                                                               event_rule["sensor_1_name"])
    value_2_data = None

    if er_type == "SENSOR_CONSTANT":
        value_2_data = core.get_constant_value(er_value_type, event_rule)
    elif er_type == "SENSOR_SENSOR":
        value_2_data = core.get_last_observation_from_sensor_name(er_value_type,
                                                                  event_rule["sensor_2_name"])

    triggered = True
    if er_comparation_type == "MORE_THAN":
        triggered = sensor_1_data > value_2_data
    elif er_comparation_type == "LESS_THAN":
        triggered = sensor_1_data < value_2_data
    elif er_comparation_type == "EQUALS":
        triggered = sensor_1_data == value_2_data
    elif er_comparation_type == "NOT_EQUALS":
        triggered = sensor_1_data != value_2_data

    print(f"EventRule {er_type} and {er_comparation_type} Checked: "
          f"ValueA is {sensor_1_data} and ValueB is {value_2_data}")

    print(f"Result is: {triggered}")

    return triggered


def execute_response_procedures(response_procedures: List):
    for response_procedure in response_procedures:
        actuator_name = response_procedure["actuator_name"]

        url = f"{BASE_URL}{API_ACTUATOR_ENDPOINT}{actuator_name}"
        print(f"Send GET to obtain Actuator {actuator_name}: {url}")
        r = requests.get(url)
        actuator = json.loads(r.content)

        url = f"{BASE_URL}{API_ACTUATION_ENDPOINT}"
        print(f"Send POST to create Actuation: {url}")
        body = {
            "time_start": utils.get_current_datetime_str(),
            "actuator_name": actuator_name,
            "actuatable_property_name": actuator["actuatable_property_name"],
        }
        r = requests.post(url, json=body)
        actuation = json.loads(r.content)
        print(actuation)

        procedure_type = response_procedure['procedure_type_name']
        url = f"{BASE_URL}{API_PROCEDURE_TYPE_NAME_ENDPOINT}{procedure_type}"
        print(f"Send GET to obtain ProcedureType {procedure_type}: {url}")
        r = requests.get(url)
        procedure = json.loads(r.content)

        if procedure["procedure_type"] == "EMAIL":
            actuators.send_email()
        elif procedure["procedure_type"] == "HTTP":
            actuators.send_http()


def execute_context_aware_rules():
    context_aware_rules = core.get_context_aware_rules()

    for context_aware_rule in context_aware_rules:
        if context_aware_rule["executing"] is True:
            ca_event_rules = core.get_event_rules_from_context_aware_rule(
                context_aware_rule["name"])
            ca_condition_rules = core.get_condition_rules_from_context_aware_rule(
                context_aware_rule["name"])

            triggered = True
            # Simple Rule
            if not ca_condition_rules:
                triggered = check_event_rule(ca_event_rules[0])
            # Complex Rule
            else:
                # TODO
                pass

            if triggered:
                ca_response_procedures = core.get_response_procedures_from_context_aware_rule(
                    context_aware_rule["name"])

                execute_response_procedures(ca_response_procedures)


def get_sensor_observations(sensor_name):
    print(f"Sending GET to obtain {sensor_name} Sensor Observations...")
    url = f"{BASE_URL}{API_SENSORS_ENDPOINT}{sensor_name}{API_SENSOR_OBSERVATIONS_ENDPOINT}"
    print(url)

    r = requests.get(url)
    sensor_observations = json.loads(r.content)["data"]
    print(sensor_observations)

    return sensor_observations


def do_actuation(context_aware_rule_name, observation_id, actuator_name):
    print(f"Sending GET to obtain {actuator_name} Actuator...")
    url = f"{BASE_URL}{API_ACTUATOR_ENDPOINT}{actuator_name}"
    print(url)

    r = requests.get(url)
    actuator = json.loads(r.content)["data"]
    print(actuator)

    print(f"HERE IS BEING DONE THE ACTUATION")
    actuators.send_email()  # TODO Make this dynamic, comparing if the actuator really does this

    print(f"Sending POST to create actuation...")
    url = f"{BASE_URL}{API_ACTUATION_ENDPOINT}"
    print(url)

    r = requests.post(url,
                      data={"observation_id": {observation_id},
                            "context_aware_rule_name": context_aware_rule_name})
    actuation = json.loads(r.content)["data"]
    print(actuation)

    return True
