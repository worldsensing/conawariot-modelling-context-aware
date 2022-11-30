import json

import requests

from src import BASE_URL, API_CONTEXT_AWARE_RULES_ENDPOINT, \
    API_CONTEXT_AWARE_RULES_COMPONENT_ENDPOINT, API_SENSORS_ENDPOINT, \
    API_SENSOR_OBSERVATIONS_ENDPOINT, API_EVENT_RULE_TYPE_NAME_ENDPOINT, API_ACTUATOR_ENDPOINT, \
    API_ACTUATION_ENDPOINT, actuators


def get_context_aware_rules():
    print("Sending GET to obtain ALL Context Aware Rules...")
    url = f"{BASE_URL}{API_CONTEXT_AWARE_RULES_ENDPOINT}"
    print(url)

    r = requests.get(url)
    context_aware_rules = json.loads(r.content)["data"]
    print(context_aware_rules)

    for context_aware_rule in context_aware_rules:
        if context_aware_rule["executing"] is True:
            ca_rule = get_context_aware_rule_components(context_aware_rule["name"])
            ca_rule_components = ca_rule["components"]

            # Simple Rule
            ca_rule_conditions = ca_rule_components["conditions"]
            if ca_rule_conditions is None:
                ca_rule_event_rule = ca_rule_components["events"][0]
                continue

            # Complex Rule
            for condition in ca_rule_conditions:
                # The condition is made up from two EventRules
                if condition["event_rule_1_name"] is not None \
                        and condition["event_rule_2_name"] is not None:
                    ca_rule_event_rule_1 = ca_rule_components["events"][0]
                    ca_rule_event_rule_2 = ca_rule_components["events"][1]
                    sensor_1_observations = get_sensor_observations(
                        ca_rule_event_rule_1["sensor_1_name"])
                    # TODO Take into account Sensor 1 and the Condition comparator

                    event_rule_type = get_event_rule_type(
                        ca_rule_event_rule_1["event_rule_type_name"])

                    # TODO Accept more than one
                    ca_rule_response_procedures = ca_rule_components["response_procedures"][0]

                    if event_rule_type["event_rule_type"] == "SENSOR_CONSTANT":
                        if event_rule_type["event_rule_comparation_type"] == "MORE_THAN":
                            if event_rule_type["event_rule_value_type"] == "INTEGER":
                                last_observation = sensor_1_observations[-1]
                                if last_observation["value"] > \
                                        ca_rule_event_rule_1["value_to_compare_integer"]:
                                    actuator_name = ca_rule_response_procedures["actuator_name"]
                                    do_actuation(context_aware_rule["name"],
                                                 last_observation["id"], actuator_name)
                                else:
                                    print("ContextAwareRule check DONE, threshold not exceeded")
                    # TODO IMPLEMENT the rest of functions

                # The condition is made up from one EventRule and one ConditionRule
                elif condition["event_rule_1_name"] is not None \
                        and condition["condition_rule_1_name"] is not None:
                    pass

                # The condition is made up from two ConditionRules
                elif condition["condition_rule_1_name"] is not None \
                        and condition["condition_rule_2_name"] is not None:
                    pass

    return context_aware_rules


def get_context_aware_rule_components(context_aware_rule_name):
    print(f"Sending GET to obtain {context_aware_rule_name} Context Aware Rule...")
    url = f"{BASE_URL}{API_CONTEXT_AWARE_RULES_ENDPOINT}{context_aware_rule_name}{API_CONTEXT_AWARE_RULES_COMPONENT_ENDPOINT}"
    print(url)

    r = requests.get(url)
    context_aware_rule = json.loads(r.content)["data"]
    print(context_aware_rule)

    return context_aware_rule


def get_event_rule_type(event_rule_type_name):
    print(f"Sending GET to obtain {event_rule_type_name} EventRuleType name...")
    url = f"{BASE_URL}{API_EVENT_RULE_TYPE_NAME_ENDPOINT}{event_rule_type_name}"
    print(url)

    r = requests.get(url)
    event_rule_type = json.loads(r.content)["data"]
    print(event_rule_type)

    return event_rule_type


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
