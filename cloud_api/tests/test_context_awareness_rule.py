import pytest

from fixtures import ContextAwareRuleFactory2DB, EventRuleTypeFactory2DB, SensorFactory2DB, \
    ThingFactory2DB, ThingTypeFactory2DB, ObservablePropertyFactory2DB, \
    FeatureOfInterestFactory2DB, LocationFactory2DB, EventRuleFactory2DB, ConditionRuleFactory2DB, \
    ResponseProcedureFactory2DB, ActuatorFactory2DB, ActuatablePropertyFactory2DB
from models.ObservableProperty import ObservableValueTypeEnum


@pytest.mark.parametrize("test_input, test_output", [
    (["BR1", True],
     ["0, BR1, True, [], [], [], []"])
])
def test_context_aware_rule_to_string(api_client, orm_client,
                                      test_input, test_output):
    context_aware_rule = ContextAwareRuleFactory2DB(
        name=test_input[0],
        executing=test_input[1])

    assert context_aware_rule.__str__() == test_output[0]


@pytest.mark.parametrize("test_input, test_output", [
    (["BR1"],
     ["0, BR1, True, [], [], [], []"])
])
def test_context_aware_rule_no_provided_executing_to_string(api_client, orm_client,
                                                            test_input, test_output):
    context_aware_rule = ContextAwareRuleFactory2DB(
        name=test_input[0])

    assert context_aware_rule.__str__() == test_output[0]


@pytest.fixture
def create_location():
    return LocationFactory2DB(name="MyLocation1")


@pytest.fixture
def create_feature_of_interest():
    return FeatureOfInterestFactory2DB(name="Roof")


@pytest.fixture
def create_actuatable_property(create_feature_of_interest):
    return ActuatablePropertyFactory2DB(name="Switch", feature_of_interest_name="Roof")


@pytest.fixture
def create_observable_property(create_feature_of_interest):
    return ObservablePropertyFactory2DB(name="RainProp", feature_of_interest_name="Roof",
                                        value_type_to_measure=ObservableValueTypeEnum.value_integer)


@pytest.fixture
def create_thing_type():
    return ThingTypeFactory2DB(name="RainModule")


@pytest.fixture
def create_thing(create_thing_type):
    return ThingFactory2DB(name="Raspberry1", type_name="RainModule")


@pytest.fixture
def create_sensor(create_thing, create_observable_property, create_location):
    return SensorFactory2DB(name="SENSOR1", thing_name="Raspberry1", location_name="MyLocation1")


@pytest.fixture
def create_actuator(create_thing, create_actuatable_property, create_location):
    return ActuatorFactory2DB(name="ACTUATOR1", thing_name="Raspberry1",
                              actuatable_property_name="Switch", location_name="MyLocation1")


@pytest.fixture
def create_event_rule_type_name():
    return EventRuleTypeFactory2DB(name="ERT1", event_rule_type="SENSOR_SENSOR",
                                   event_rule_comparation_type="LESS_THAN")


@pytest.mark.parametrize("test_input, test_output", [
    (["BR1", True],
     ["0, BR1, True, [], [], [], []"])
])
def test_context_aware_rule_with_components_to_string(api_client, orm_client,
                                                      create_event_rule_type_name, create_sensor,
                                                      create_actuator,
                                                      test_input, test_output):
    context_aware_rule = ContextAwareRuleFactory2DB(
        name=test_input[0],
        executing=test_input[1])

    event_rule_1 = EventRuleFactory2DB(name="ER1", context_aware_rule_name=context_aware_rule.name,
                                       event_rule_type_name="ERT1", sensor_1_name="SENSOR1",
                                       value_to_compare_integer=1)

    event_rule_2 = EventRuleFactory2DB(name="ER2", context_aware_rule_name=context_aware_rule.name,
                                       event_rule_type_name="ERT1", sensor_1_name="SENSOR1",
                                       value_to_compare_integer=2)

    condition_rule = ConditionRuleFactory2DB(name="CR1",
                                             context_aware_rule_name=context_aware_rule.name,
                                             event_rule_1_name="ER1",
                                             event_rule_2_name="ER2",
                                             condition_comparation_type="AND")

    response_procedure = ResponseProcedureFactory2DB(name="RP1",
                                                     context_aware_rule_name=context_aware_rule.name,
                                                     procedure_type_name="PT1",
                                                     actuator_name="ACTUATOR1")

    assert context_aware_rule.id == 0
    assert context_aware_rule.name == "BR1"
    assert context_aware_rule.executing is True
    assert context_aware_rule.event_rules[0].to_json() == {'id': 0, 'name': 'ER1',
                                                           'context_aware_rule_name': 'BR1',
                                                           'event_rule_type_name': 'ERT1',
                                                           'sensor_1_name': 'SENSOR1',
                                                           'sensor_2_name': None,
                                                           'value_to_compare_boolean': None,
                                                           'value_to_compare_string': None,
                                                           'value_to_compare_integer': 1,
                                                           'value_to_compare_float': None}
    assert context_aware_rule.event_rules[1].to_json() == {'id': 1, 'name': 'ER2',
                                                           'context_aware_rule_name': 'BR1',
                                                           'event_rule_type_name': 'ERT1',
                                                           'sensor_1_name': 'SENSOR1',
                                                           'sensor_2_name': None,
                                                           'value_to_compare_boolean': None,
                                                           'value_to_compare_string': None,
                                                           'value_to_compare_integer': 2,
                                                           'value_to_compare_float': None}
    assert context_aware_rule.condition_rules[0].to_json() == {'id': 0, 'name': 'CR1',
                                                               'context_aware_rule_name': 'BR1',
                                                               'event_rule_1_name': 'ER1',
                                                               'event_rule_2_name': 'ER2',
                                                               'condition_rule_1_name': None,
                                                               'condition_rule_2_name': None,
                                                               'condition_comparation_type': "AND"}
    assert context_aware_rule.response_procedure[0].to_json() == {'id': 0,
                                                                  'name': 'RP1',
                                                                  'context_aware_rule_name': 'BR1',
                                                                  'procedure_type_name': 'PT1',
                                                                  'actuator_name': 'ACTUATOR1'}
