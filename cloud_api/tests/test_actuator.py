import pytest

from fixtures import FeatureOfInterestFactory2DB, ActuatablePropertyFactory2DB, ActuatorFactory2DB, \
    LocationFactory2DB, ThingTypeFactory2DB, ThingFactory2DB


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
def create_thing_type():
    return ThingTypeFactory2DB(name="RainModule")


@pytest.fixture
def create_thing(create_thing_type):
    return ThingFactory2DB(name="RainModuleA", type_name="RainModule")


@pytest.mark.parametrize("test_input, test_output", [
    (["RainModuleA", "LightSwitch", "Leg", None],
     ["0, RainModuleA, LightSwitch, Leg, None, []"])
])
def test_actuator_to_string(api_client, orm_client, create_thing, create_actuatable_property,
                            create_location,
                            test_input, test_output):
    actuator = ActuatorFactory2DB(thing_name=test_input[0],
                                  name=test_input[1],
                                  actuatable_property_name=test_input[2],
                                  location_name=test_input[3])

    assert actuator.__str__() == test_output[0]
