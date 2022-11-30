import pytest

from fixtures import ThingFactory2DB, ObservationBooleanFactory2DB, ObservationStringFactory2DB, \
    ObservationIntegerFactory2DB, ObservationFloatFactory2DB, ThingTypeFactory2DB, SensorFactory2DB


@pytest.fixture
def create_thing_type():
    return ThingTypeFactory2DB(name="Inclinometer")


@pytest.fixture
def create_thing(create_thing_type):
    return ThingFactory2DB(name="ABC-1001", type_name="Inclinometer")


@pytest.fixture
def create_sensor(create_thing):
    return SensorFactory2DB(thing_name="ABC-1001", name="RainSensorA")


@pytest.mark.parametrize("test_input, test_output", [
    (["RainSensorA", True, "2020-03-19T12:00:00+00:00"],
     ["0, RainSensorA, True, 2020-03-19T12:00:00+00:00, None"])
])
def test_obs_boolean_to_string(api_client, orm_client, create_sensor,
                               test_input, test_output):
    observation = ObservationBooleanFactory2DB(sensor_name=test_input[0],
                                               value=test_input[1],
                                               time_start=test_input[2])

    assert observation.__str__() == test_output[0]


@pytest.mark.parametrize("test_input, test_output", [
    (["RainSensorA", "TestString", "2020-03-19T12:00:00+00:00"],
     ["0, RainSensorA, TestString, 2020-03-19T12:00:00+00:00, None"])
])
def test_obs_string_to_string(api_client, orm_client, create_sensor,
                              test_input, test_output):
    observation = ObservationStringFactory2DB(sensor_name=test_input[0],
                                              value=test_input[1],
                                              time_start=test_input[2])

    assert observation.__str__() == test_output[0]


@pytest.mark.parametrize("test_input, test_output", [
    (["RainSensorA", 1, "2020-03-19T12:00:00+00:00"],
     ["0, RainSensorA, 1, 2020-03-19T12:00:00+00:00, None"])
])
def test_obs_integer_to_string(api_client, orm_client, create_sensor,
                               test_input, test_output):
    observation = ObservationIntegerFactory2DB(sensor_name=test_input[0],
                                               value=test_input[1],
                                               time_start=test_input[2])

    assert observation.__str__() == test_output[0]


@pytest.mark.parametrize("test_input, test_output", [
    (["RainSensorA", 1.1, "2020-03-19T12:00:00+00:00"],
     ["0, RainSensorA, 1.1, 2020-03-19T12:00:00+00:00, None"])
])
def test_obs_float_to_string(api_client, orm_client, create_sensor,
                             test_input, test_output):
    observation = ObservationFloatFactory2DB(sensor_name=test_input[0],
                                             value=test_input[1],
                                             time_start=test_input[2])

    assert observation.__str__() == test_output[0]


@pytest.mark.parametrize("test_input, test_output", [
    (["RainSensorA", True, "2020-03-19T12:00:00+02:00"],
     ["0, RainSensorA, True, 2020-03-19T10:00:00+00:00, None"])
])
def test_obs_boolean_time_start_different_timezone_to_string(api_client, orm_client, create_sensor,
                                                             test_input, test_output):
    observation = ObservationBooleanFactory2DB(sensor_name=test_input[0],
                                               value=test_input[1],
                                               time_start=test_input[2])

    assert observation.__str__() == test_output[0]
