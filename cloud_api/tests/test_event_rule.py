import pytest

from fixtures import ContextAwareRuleFactory2DB, EventRuleFactory2DB, \
    EventRuleTypeFactory2DB, SensorFactory2DB, ThingFactory2DB, ThingTypeFactory2DB, \
    ObservablePropertyFactory2DB, FeatureOfInterestFactory2DB, LocationFactory2DB
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
def create_sensor(create_thing, create_observable_property, create_location):
    return SensorFactory2DB(name="SENSOR1", thing_name="Raspberry1", location_name="MyLocation1")


@pytest.fixture
def create_event_rule_type_name():
    return EventRuleTypeFactory2DB(name="ERT1", event_rule_type="SENSOR_SENSOR",
                                   event_rule_comparation_type="LESS_THAN")


@pytest.fixture
def create_context_aware_rule():
    return ContextAwareRuleFactory2DB(name="BR1")


@pytest.mark.parametrize("test_input, test_output", [
    (["ER1", "BR1", "ERT1", "SENSOR1", 1],
     ["0, ER1, BR1, ERT1, SENSOR1, None, None, None, 1, None"])
])
def test_event_rule_to_string(api_client, orm_client, create_context_aware_rule,
                              create_event_rule_type_name, create_sensor,
                              test_input, test_output):
    event_rule = EventRuleFactory2DB(
        name=test_input[0],
        context_aware_rule_name=test_input[1],
        event_rule_type_name=test_input[2],
        sensor_1_name=test_input[3],
        value_to_compare_integer=test_input[4])

    assert event_rule.__str__() == test_output[0]
