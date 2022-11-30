import pytest

from fixtures import ConditionRuleFactory2DB, ContextAwareRuleFactory2DB, SensorFactory2DB, \
    ThingTypeFactory2DB, LocationFactory2DB, ThingFactory2DB, FeatureOfInterestFactory2DB, \
    ObservablePropertyFactory2DB, EventRuleFactory2DB, EventRuleTypeFactory2DB
from models.ObservableProperty import ObservableValueTypeEnum


@pytest.fixture
def create_location():
    return LocationFactory2DB(name="MyLocation1")


@pytest.fixture
def create_feature_of_interest():
    return FeatureOfInterestFactory2DB(name="Person")


@pytest.fixture
def create_observable_property(create_feature_of_interest):
    return ObservablePropertyFactory2DB(name="RainProp", feature_of_interest_name="Person",
                                        value_type_to_measure=ObservableValueTypeEnum.value_integer)


@pytest.fixture
def create_thing_type():
    return ThingTypeFactory2DB(name="RainModule")


@pytest.fixture
def create_thing(create_thing_type):
    return ThingFactory2DB(name="Raspberry1", type_name="RainModule")


@pytest.fixture
def create_sensor_1(create_thing, create_observable_property, create_location):
    return SensorFactory2DB(name="SENSOR1", thing_name="Raspberry1", location_name="MyLocation1")


@pytest.fixture
def create_sensor_2(create_thing, create_observable_property, create_location):
    return SensorFactory2DB(name="SENSOR2", thing_name="Raspberry1", location_name="MyLocation1")


@pytest.fixture
def create_context_aware_rule():
    return ContextAwareRuleFactory2DB(name="BR1")


@pytest.fixture
def create_event_rule_type_name_1():
    return EventRuleTypeFactory2DB(name="ER1", event_rule_type="SENSOR_SENSOR",
                                   event_rule_comparation_type="LESS_THAN")


@pytest.fixture
def create_event_rule_type_name_2():
    return EventRuleTypeFactory2DB(name="ER2", event_rule_type="SENSOR_CONSTANT",
                                   event_rule_comparation_type="MORE_THAN",
                                   event_rule_value_type="INTEGER")


@pytest.fixture
def create_event_rule_1(create_context_aware_rule, create_event_rule_type_name_1,
                        create_sensor_1, create_sensor_2):
    return EventRuleFactory2DB(name="ER1", context_aware_rule_name="BR1",
                               event_rule_type_name="ER1", sensor_1_name="SENSOR1",
                               sensor_2_name="SENSOR2")


@pytest.fixture
def create_event_rule_2(create_context_aware_rule, create_event_rule_type_name_2, create_sensor_1):
    return EventRuleFactory2DB(name="ER2", context_aware_rule_name="BR1",
                               event_rule_type_name="ER2", sensor_1_name="SENSOR1",
                               value_to_compare_integer=1)


@pytest.mark.parametrize("test_input, test_output", [
    (["CR1", "BR1", "ER1", "ER2", "AND"],
     ["0, CR1, ER1, ER2, None, None, AND"])
])
def test_condition_rule_to_string(api_client, orm_client, create_context_aware_rule,
                                  create_event_rule_1, create_event_rule_2,
                                  test_input, test_output):
    condition_rule = ConditionRuleFactory2DB(
        name=test_input[0],
        context_aware_rule_name=test_input[1],
        event_rule_1_name=test_input[2],
        event_rule_2_name=test_input[3],
        condition_comparation_type=test_input[4])

    assert condition_rule.__str__() == test_output[0]

# TODO Create tests with more than two EventRules/ConditionRules
