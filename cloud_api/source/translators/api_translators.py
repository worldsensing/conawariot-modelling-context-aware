# -*- coding: utf-8 -*-
from translators import model_translators


def actuatable_property_translator(actuatable_property_from_db):
    return {
        "id": actuatable_property_from_db.id,
        "name": actuatable_property_from_db.name,
        "feature_of_interest_name": actuatable_property_from_db.feature_of_interest_name,
    }


def actuation_translator(actuation_from_db):
    return {
        "id": actuation_from_db.id,
        "observation_id": actuation_from_db.observation_id,
        "context_aware_rule_name": actuation_from_db.context_aware_rule_name,
        "time_start": model_translators.translate_datetime(actuation_from_db.time_start),
        "time_end": model_translators.translate_datetime(actuation_from_db.time_end),
    }


def actuator_translator(actuator_from_db):
    return {
        "id": actuator_from_db.id,
        "thing_name": actuator_from_db.thing_name,
        "name": actuator_from_db.name,
        "actuatable_property_name": actuator_from_db.actuatable_property_name,
        "location_name": actuator_from_db.location_name,
    }


def condition_rule_translator(condition_rule_from_db):
    return {
        "id": condition_rule_from_db.id,
        "name": condition_rule_from_db.name,
        "context_aware_rule_name": condition_rule_from_db.context_aware_rule_name,
        "event_rule_1_name": condition_rule_from_db.event_rule_1_name,
        "event_rule_2_name": condition_rule_from_db.event_rule_2_name,
        "condition_rule_1_name": condition_rule_from_db.condition_rule_1_name,
        "condition_rule_2_name": condition_rule_from_db.condition_rule_2_name,
        "condition_comparation_type": condition_rule_from_db.condition_comparation_type.value,
    }


def context_aware_rule_translator(context_aware_rule_from_db):
    return {
        "id": context_aware_rule_from_db.id,
        "name": context_aware_rule_from_db.name,
        "executing": context_aware_rule_from_db.executing,
    }


def context_aware_rule_components_translator(context_aware_rule_from_db):
    events = []
    for event in context_aware_rule_from_db.event_rules:
        events.append(event.to_json())

    conditions = []
    for condition in context_aware_rule_from_db.condition_rules:
        conditions.append(condition.to_json())

    response_procedures = []
    for response_procedure in context_aware_rule_from_db.response_procedure:
        response_procedures.append(response_procedure.to_json())

    return {
        "id": context_aware_rule_from_db.id,
        "name": context_aware_rule_from_db.name,
        "executing": context_aware_rule_from_db.executing,
        "components": {
            "events": events,
            "conditions": conditions,
            "response_procedures": response_procedures
        }
    }


def event_rule_translator(event_rule_from_db):
    return {
        "id": event_rule_from_db.id,
        "name": event_rule_from_db.name,
        "context_aware_rule_name": event_rule_from_db.context_aware_rule_name,
        "sensor_1_name": event_rule_from_db.sensor_1_name,
        "sensor_2_name": event_rule_from_db.sensor_2_name,
        "value_to_compare_boolean": event_rule_from_db.value_to_compare_boolean,
        "value_to_compare_string": event_rule_from_db.value_to_compare_string,
        "value_to_compare_integer": event_rule_from_db.value_to_compare_integer,
        "value_to_compare_float": event_rule_from_db.value_to_compare_float,
    }


def event_rule_type_translator(event_rule_type_from_db):
    return {
        "id": event_rule_type_from_db.id,
        "name": event_rule_type_from_db.name,
        "event_rule_type": event_rule_type_from_db.event_rule_type.value,
        "event_rule_comparation_type": event_rule_type_from_db.event_rule_comparation_type.value,
        "event_rule_value_type": event_rule_type_from_db.event_rule_value_type.value,
    }


def feature_of_interest_translator(feature_of_interest_from_db):
    return {
        "id": feature_of_interest_from_db.id,
        "name": feature_of_interest_from_db.name,
        "location_name": feature_of_interest_from_db.location_name,
    }


def location_translator(location_from_db):
    return {
        "id": location_from_db.id,
        "name": location_from_db.name,
        "latlng": location_from_db.latlng,
    }


def observable_property_translator(observable_property_from_db):
    return {
        "id": observable_property_from_db.id,
        "name": observable_property_from_db.name,
        "value_type_to_measure": observable_property_from_db.value_type_to_measure.value,
        "feature_of_interest_name": observable_property_from_db.feature_of_interest_name,
    }


def observation_translator(observation_from_db):
    return {
        "id": observation_from_db.id,
        "sensor_name": observation_from_db.sensor_name,
        "time_start": model_translators.translate_datetime(observation_from_db.time_start),
        "time_end": model_translators.translate_datetime(observation_from_db.time_end),
        "value": observation_from_db.value,
    }


def platform_translator(platform_from_db):
    return {
        "id": platform_from_db.id,
        "name": platform_from_db.name,
        "location_name": platform_from_db.location_name,
    }


def response_procedure_translator(response_procedure_from_db):
    return {
        "id": response_procedure_from_db.id,
        "name": response_procedure_from_db.name,
        "context_aware_rule_name": response_procedure_from_db.context_aware_rule_name,
        "procedure_type_name": response_procedure_from_db.procedure_type_name,
        "actuator_name": response_procedure_from_db.actuator_name,
    }


def sensor_translator(sensor_from_db):
    return {
        "id": sensor_from_db.id,
        "thing_name": sensor_from_db.thing_name,
        "name": sensor_from_db.name,
        "observable_property_name": sensor_from_db.observable_property_name,
        "location_name": sensor_from_db.location_name,
    }


def thing_translator(thing_from_db):
    return {
        "id": thing_from_db.id,
        "name": thing_from_db.name,
        "type_name": thing_from_db.type_name,
        "location_name": thing_from_db.location_name,
    }


def thing_type_translator(thing_type_from_db):
    return {
        "id": thing_type_from_db.id,
        "name": thing_type_from_db.name,
    }
