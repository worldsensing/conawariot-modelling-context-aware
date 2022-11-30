import pytest

from fixtures import ThingFactory2DB, ThingTypeFactory2DB, ObservablePropertyFactory2DB, \
    SensorFactory2DB, FeatureOfInterestFactory2DB, LocationFactory2DB
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
    return ThingFactory2DB(name="RainModuleA", type_name="RainModule")


@pytest.mark.parametrize("test_input, test_output", [
    (["RainSensor", "RainModuleA", "RainProp", "MyLocation1"],
     ["0, RainSensor, RainModuleA, RainProp, MyLocation1, []"])
])
def test_sensor_to_string(api_client, orm_client, create_thing, create_observable_property,
                          create_location,
                          test_input, test_output):
    sensor = SensorFactory2DB(name=test_input[0],
                              thing_name=test_input[1],
                              observable_property_name=test_input[2],
                              location_name=test_input[3])

    assert sensor.__str__() == test_output[0]
