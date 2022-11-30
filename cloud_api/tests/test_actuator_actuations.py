import pytest

from fixtures import FeatureOfInterestFactory2DB, ActuatablePropertyFactory2DB, ActuatorFactory2DB, \
    LocationFactory2DB, ThingTypeFactory2DB, ThingFactory2DB, SensorFactory2DB, \
    ObservationFactory2DB, ContextAwareRuleFactory2DB, ActuatorActuationFactory2DB, \
    ActuationFactory2DB


@pytest.fixture
def create_location():
    return LocationFactory2DB(name="MyLocation2")


@pytest.fixture
def create_feature_of_interest(create_location):
    return FeatureOfInterestFactory2DB(name="Person")


@pytest.fixture
def create_actuatable_property(create_feature_of_interest):
    return ActuatablePropertyFactory2DB(name="Leg", feature_of_interest_name="Person")


@pytest.fixture
def create_actuator(create_thing, create_actuatable_property, create_location):
    return ActuatorFactory2DB(thing_name="RainModuleA", name="LightSwitch",
                              actuatable_property_name="Leg", location_name=None)


@pytest.fixture
def create_context_aware_rule():
    return ContextAwareRuleFactory2DB(name="Rule1", executing=True)


@pytest.fixture
def create_thing_type():
    return ThingTypeFactory2DB(name="RainModule")


@pytest.fixture
def create_thing(create_thing_type):
    return ThingFactory2DB(name="RainModuleA", type_name="RainModule")


@pytest.fixture
def create_sensor(create_thing):
    return SensorFactory2DB(thing_name="RainModuleA", name="RainSensorA")


@pytest.fixture
def create_observation(create_sensor):
    return ObservationFactory2DB(sensor_name="RainSensorA", time_start="2020-03-19T12:00:00+00:00")


@pytest.fixture
def create_actuation(create_observation, create_context_aware_rule):
    return ActuationFactory2DB(observation_id=0, context_aware_rule_name="Rule1",
                               time_start="2020-03-18T12:00:00+00:00")


@pytest.mark.parametrize("test_input, test_output", [
    ([0, "LightSwitch"],
     ["LightSwitch, 0"])
])
def test_actuator_actuations_to_string(api_client, orm_client, create_actuator, create_actuation,
                                       test_input, test_output):
    actuator_actuations = ActuatorActuationFactory2DB(actuation_id=test_input[0],
                                                      actuator_name=test_input[1])

    assert actuator_actuations.__str__() == test_output[0]
