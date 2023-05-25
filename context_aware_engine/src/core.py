import json

import requests
from src import BASE_URL, API_CONTEXT_AWARE_RULES_ENDPOINT, \
    API_CONTEXT_AWARE_RULES_EVENT_RULES_ENDPOINT, API_CONTEXT_AWARE_RULES_CONDITION_RULES_ENDPOINT, \
    API_EVENT_RULE_TYPE_NAME_ENDPOINT, API_SENSOR_OBSERVATIONS_ENDPOINT, API_SENSORS_ENDPOINT, \
    API_CONTEXT_AWARE_RULES_RESPONSE_PROCEDURES_ENDPOINT


def get_context_aware_rules():
    url = f"{BASE_URL}{API_CONTEXT_AWARE_RULES_ENDPOINT}"
    print(f"Send GET to obtain ALL ContextAwareRules: {url}")

    r = requests.get(url)
    context_aware_rules = json.loads(r.content)

    return context_aware_rules


def get_event_rules_from_context_aware_rule(context_aware_rule_name: str):
    url = f"{BASE_URL}{API_CONTEXT_AWARE_RULES_ENDPOINT}" \
          f"{context_aware_rule_name}/{API_CONTEXT_AWARE_RULES_EVENT_RULES_ENDPOINT}"
    print(f"Send GET to obtain EventRules from ContextAwareRule {context_aware_rule_name}: {url}")

    r = requests.get(url)
    event_rules = json.loads(r.content)

    return event_rules


def get_event_rule_type(event_rule_type_name: str):
    url = f"{BASE_URL}{API_EVENT_RULE_TYPE_NAME_ENDPOINT}{event_rule_type_name}"
    print(f"Send GET to obtain EventRuleType {event_rule_type_name}: {url}")

    r = requests.get(url)
    event_rule_type = json.loads(r.content)

    return event_rule_type


def get_condition_rules_from_context_aware_rule(context_aware_rule_name: str):
    url = f"{BASE_URL}{API_CONTEXT_AWARE_RULES_ENDPOINT}" \
          f"{context_aware_rule_name}/{API_CONTEXT_AWARE_RULES_CONDITION_RULES_ENDPOINT}"
    print(
        f"Send GET to obtain ConditionRules from ContextAwareRule {context_aware_rule_name}: {url}")

    r = requests.get(url)
    condition_rules = json.loads(r.content)

    return condition_rules


def get_response_procedures_from_context_aware_rule(context_aware_rule_name: str):
    url = f"{BASE_URL}{API_CONTEXT_AWARE_RULES_ENDPOINT}" \
          f"{context_aware_rule_name}/{API_CONTEXT_AWARE_RULES_RESPONSE_PROCEDURES_ENDPOINT}"
    print(
        f"Send GET to obtain ResponseProcedures from ContextAwareRule {context_aware_rule_name}: {url}")

    r = requests.get(url)
    response_procedures = json.loads(r.content)

    return response_procedures


def get_last_observation_from_sensor_name(event_rule_value_type: str, sensor_name: str):
    url = f"{BASE_URL}{API_SENSOR_OBSERVATIONS_ENDPOINT}{API_SENSORS_ENDPOINT}{sensor_name}"
    print(f"Send GET to obtain Observations from Sensor {sensor_name}: {url}")

    r = requests.get(url)
    observations = json.loads(r.content)

    if observations:
        observation = observations[-1]

        if event_rule_value_type == "INTEGER":
            return observation["value_int"]
        if event_rule_value_type == "BOOLEAN":
            return observation["value_bool"]
        if event_rule_value_type == "STRING":
            return observation["value_str"]
        if event_rule_value_type == "FLOAT":
            return observation["value_float"]

    return None


def get_constant_value(event_rule_value_type: str, event: dict):
    if event_rule_value_type == "INTEGER":
        return event["value_to_compare_integer"]
    if event_rule_value_type == "BOOLEAN":
        return event["value_to_compare_boolean"]
    if event_rule_value_type == "STRING":
        return event["value_to_compare_string"]
    if event_rule_value_type == "FLOAT":
        return event["value_to_compare_float"]

    return None
