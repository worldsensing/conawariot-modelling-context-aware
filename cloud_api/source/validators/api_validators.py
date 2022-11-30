from models.ConditionRule import ConditionRuleComparationTypeEnum
from models.EventRuleType import EventRuleTypeEnum, EventRuleComparationTypeEnum, \
    EventRuleValueTypeEnum
from models.ObservableProperty import ObservableValueTypeEnum


class ActuatablePropertyValidator:
    @staticmethod
    def is_name_valid(value):
        return isinstance(value, str) and not value == ""

    @staticmethod
    def is_feature_of_interest_name_valid(value):
        return isinstance(value, str) and not value == ""


class ActuationValidator:
    @staticmethod
    def is_observation_id_valid(value):
        return isinstance(value, int)

    @staticmethod
    def is_context_aware_rule_name_valid(value):
        return isinstance(value, str) and not value == ""

    @staticmethod
    def is_time_start_valid(value):
        return isinstance(value, str) and not value == ""

    @staticmethod
    def is_time_end_valid(value):
        return isinstance(value, str) and not value == ""


class ActuatorValidator:
    @staticmethod
    def is_thing_name_valid(value):
        return isinstance(value, str)

    @staticmethod
    def is_name_valid(value):
        return isinstance(value, str) and not value == ""

    @staticmethod
    def is_actuatable_property_name_valid(value):
        return isinstance(value, str) and not value == ""

    @staticmethod
    def is_location_name_valid(value):
        return isinstance(value, str) and not value == ""


class ConditionRuleValidator:
    @staticmethod
    def is_name_valid(value):
        return isinstance(value, str) and not value == ""

    @staticmethod
    def is_context_aware_rule_name_valid(value):
        return isinstance(value, str) and not value == "" and \
               ContextAwareRuleValidator.is_name_valid(value)

    @staticmethod
    def is_event_rule_name_valid(value):
        return isinstance(value, str) and not value == "" and \
               EventRuleValidator.is_name_valid(value)

    @staticmethod
    def is_condition_comparation_type_valid(value):
        values = [item.value for item in ConditionRuleComparationTypeEnum]
        return isinstance(value, str) and value in values


class ContextAwareRuleValidator:
    @staticmethod
    def is_name_valid(value):
        return isinstance(value, str) and not value == ""

    @staticmethod
    def is_executing_valid(value):
        return isinstance(value, bool)


class EventRuleValidator:
    @staticmethod
    def is_name_valid(value):
        return isinstance(value, str) and not value == ""

    @staticmethod
    def is_context_aware_rule_name_valid(value):
        return isinstance(value, str) and not value == "" and \
               ContextAwareRuleValidator.is_name_valid(value)

    @staticmethod
    def is_event_rule_type_name_valid(value):
        return isinstance(value, str) and not value == "" and \
               EventRuleTypeValidator.is_name_valid(value)

    @staticmethod
    def is_sensor_name_valid(value):
        return isinstance(value, str) and not value == "" and \
               SensorValidator.is_name_valid(value)

    @staticmethod
    def is_value_to_compare_boolean_valid(value):
        return isinstance(value, bool)

    @staticmethod
    def is_value_to_compare_string_valid(value):
        return isinstance(value, str)

    @staticmethod
    def is_value_to_compare_integer_valid(value):
        return isinstance(value, int)

    @staticmethod
    def is_value_to_compare_float_valid(value):
        return isinstance(value, float)


class EventRuleTypeValidator:
    @staticmethod
    def is_name_valid(value):
        return isinstance(value, str) and not value == ""

    @staticmethod
    def is_event_rule_type_valid(value):
        values = [item.value for item in EventRuleTypeEnum]
        return isinstance(value, str) and value in values

    @staticmethod
    def is_event_rule_comparation_type_valid(value):
        values = [item.value for item in EventRuleComparationTypeEnum]
        return isinstance(value, str) and value in values

    @staticmethod
    def is_event_rule_value_type_valid(value):
        values = [item.value for item in EventRuleValueTypeEnum]
        return isinstance(value, str) and value in values


class FeatureOfInterestValidator:
    @staticmethod
    def is_name_valid(value):
        return isinstance(value, str)

    @staticmethod
    def is_location_name_valid(value):
        return isinstance(value, str) and not value == ""


class LocationValidator:
    @staticmethod
    def is_name_valid(value):
        return isinstance(value, str) and not value == ""

    @staticmethod
    def is_latlng_valid(value):
        return isinstance(value, str) and not value == "" and len(value.split(",")) == 2


class ObservablePropertyValidator:
    @staticmethod
    def is_name_valid(value):
        return isinstance(value, str) and not value == ""

    @staticmethod
    def is_value_type_to_measure_valid(value):
        values = [item.value for item in ObservableValueTypeEnum]
        return isinstance(value, str) and value in values

    @staticmethod
    def is_feature_of_interest_name_valid(value):
        return isinstance(value, str)


class ObservationValidator:
    @staticmethod
    def is_sensor_name_valid(value):
        return isinstance(value, str) and not value == ""

    @staticmethod
    def is_time_start_valid(value):
        return isinstance(value, str) and not value == ""

    @staticmethod
    def is_time_end_valid(value):
        return isinstance(value, str) and not value == ""

    @staticmethod
    def is_value_valid(value):
        return isinstance(value, str) and not value == ""


class PlatformValidator:
    @staticmethod
    def is_name_valid(value):
        return isinstance(value, str)

    @staticmethod
    def is_location_name_valid(value):
        return isinstance(value, str) and not value == ""


class ResponseProcedureValidator:
    @staticmethod
    def is_name_valid(value):
        return isinstance(value, str) and not value == ""

    @staticmethod
    def is_context_aware_rule_name_valid(value):
        return isinstance(value, str) and not value == "" and \
               ContextAwareRuleValidator.is_name_valid(value)

    @staticmethod
    def is_procedure_type_name_valid(value):
        return isinstance(value, str) and not value == ""

    @staticmethod
    def is_actuator_name_valid(value):
        return isinstance(value, str) and not value == "" and \
               ActuatorValidator.is_name_valid(value)


class SensorValidator:
    @staticmethod
    def is_thing_name_valid(value):
        return isinstance(value, str)

    @staticmethod
    def is_name_valid(value):
        return isinstance(value, str)

    @staticmethod
    def is_observable_property_name_valid(value):
        return isinstance(value, str)

    @staticmethod
    def is_location_name_valid(value):
        return isinstance(value, str) and not value == ""


class ThingValidator:
    @staticmethod
    def is_name_valid(value):
        return isinstance(value, str) and not value == ""

    @staticmethod
    def is_type_name_valid(value):
        return isinstance(value, str) and not value == ""

    @staticmethod
    def is_location_name_valid(value):
        return isinstance(value, str) and not value == ""


class ThingTypeValidator:
    @staticmethod
    def is_name_valid(value):
        return isinstance(value, str) and not value == ""
