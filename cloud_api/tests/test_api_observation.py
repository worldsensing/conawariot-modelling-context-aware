import json

import pytest

from fixtures import ThingFactory2DB, ThingTypeFactory2DB, ObservationBooleanFactory2DB, \
    ObservationStringFactory2DB, ObservationIntegerFactory2DB, ObservationFloatFactory2DB, \
    SensorFactory2DB, ObservationBooleanDictFactory, ObservationStringDictFactory, \
    ObservationIntegerDictFactory, ObservationFloatDictFactory, ObservablePropertyFactory2DB, \
    FeatureOfInterestFactory2DB
from models import Observation, ObservationBoolean, ObservationString, ObservationInteger, \
    ObservationFloat
from models.ObservableProperty import ObservableValueTypeEnum
from translators import model_translators


def assert_observations(observation_api, observation_db):
    # assert observation_db["id"] == observation_api["id"]
    assert observation_db["sensor_name"] == observation_api["sensor_name"]
    assert str(observation_db["value"]) == str(observation_api["value"])
    if isinstance(observation_db["time_start"], str):
        assert observation_db["time_start"] == observation_api["time_start"]
    else:
        assert model_translators.translate_datetime(observation_db["time_start"]) == \
               observation_api["time_start"]
    # TODO Check time_end


@pytest.fixture
def create_thing_type():
    return ThingTypeFactory2DB(name="Inclinometer")


@pytest.fixture
def create_thing(create_thing_type):
    return ThingFactory2DB(name="ABC-1001", type_name="Inclinometer")


@pytest.fixture
def create_feature_of_interest():
    return FeatureOfInterestFactory2DB(name="Person")


@pytest.fixture
def create_observable_property_a(create_feature_of_interest):
    return ObservablePropertyFactory2DB(name="RainPropA", feature_of_interest_name="Person",
                                        value_type_to_measure=ObservableValueTypeEnum.value_boolean)


@pytest.fixture
def create_sensor_a(create_thing, create_observable_property_a):
    return SensorFactory2DB(thing_name="ABC-1001", name="SensorA",
                            observable_property_name="RainPropA")


@pytest.fixture
def create_observable_property_b(create_feature_of_interest):
    return ObservablePropertyFactory2DB(name="RainPropB", feature_of_interest_name="Person",
                                        value_type_to_measure=ObservableValueTypeEnum.value_string)


@pytest.fixture
def create_sensor_b(create_thing, create_observable_property_b):
    return SensorFactory2DB(thing_name="ABC-1001", name="SensorB",
                            observable_property_name="RainPropB")


@pytest.fixture
def create_observable_property_c(create_feature_of_interest):
    return ObservablePropertyFactory2DB(name="RainPropC", feature_of_interest_name="Person",
                                        value_type_to_measure=ObservableValueTypeEnum.value_integer)


@pytest.fixture
def create_sensor_c(create_thing, create_observable_property_c):
    return SensorFactory2DB(thing_name="ABC-1001", name="SensorC",
                            observable_property_name="RainPropC")


@pytest.fixture
def create_observable_property_d(create_feature_of_interest):
    return ObservablePropertyFactory2DB(name="RainPropD", feature_of_interest_name="Person",
                                        value_type_to_measure=ObservableValueTypeEnum.value_float)


@pytest.fixture
def create_sensor_d(create_thing, create_observable_property_d):
    return SensorFactory2DB(thing_name="ABC-1001", name="SensorD",
                            observable_property_name="RainPropD")


@pytest.mark.parametrize("test_input, test_input_2, test_input_3, test_input_4", [
    (["SensorA", True, "2020-03-18T12:00:00+00:00"],
     ["SensorB", "SAMPLEVALUE", "2020-03-18T12:00:00+00:00"],
     ["SensorC", 1, "2020-03-18T12:00:00+00:00"],
     ["SensorD", 0.2, "2020-03-18T12:02:00+00:00"])
])
def test_get_observations_all(api_client, orm_client, create_sensor_a, create_sensor_b,
                              create_sensor_c, create_sensor_d,
                              test_input, test_input_2, test_input_3, test_input_4):
    assert orm_client.session.query(Observation).count() == 0
    assert orm_client.session.query(ObservationBoolean).count() == 0
    assert orm_client.session.query(ObservationString).count() == 0
    assert orm_client.session.query(ObservationInteger).count() == 0
    assert orm_client.session.query(ObservationFloat).count() == 0
    observation_1 = ObservationBooleanFactory2DB(sensor_name=test_input[0],
                                                 value=test_input[1],
                                                 time_start=test_input[2])
    assert orm_client.session.query(Observation).count() == 1
    assert orm_client.session.query(ObservationBoolean).count() == 1
    assert orm_client.session.query(ObservationString).count() == 0
    assert orm_client.session.query(ObservationInteger).count() == 0
    assert orm_client.session.query(ObservationFloat).count() == 0
    observation_2 = ObservationStringFactory2DB(sensor_name=test_input_2[0],
                                                value=test_input_2[1],
                                                time_start=test_input_2[2])
    assert orm_client.session.query(Observation).count() == 2
    assert orm_client.session.query(ObservationBoolean).count() == 1
    assert orm_client.session.query(ObservationString).count() == 1
    assert orm_client.session.query(ObservationInteger).count() == 0
    assert orm_client.session.query(ObservationFloat).count() == 0
    observation_3 = ObservationIntegerFactory2DB(sensor_name=test_input_3[0],
                                                 value=test_input_3[1],
                                                 time_start=test_input_3[2])
    assert orm_client.session.query(Observation).count() == 3
    assert orm_client.session.query(ObservationBoolean).count() == 1
    assert orm_client.session.query(ObservationString).count() == 1
    assert orm_client.session.query(ObservationInteger).count() == 1
    assert orm_client.session.query(ObservationFloat).count() == 0
    observation_4 = ObservationFloatFactory2DB(sensor_name=test_input_4[0],
                                               value=test_input_4[1],
                                               time_start=test_input_4[2])
    assert orm_client.session.query(Observation).count() == 4
    assert orm_client.session.query(ObservationBoolean).count() == 1
    assert orm_client.session.query(ObservationString).count() == 1
    assert orm_client.session.query(ObservationInteger).count() == 1
    assert orm_client.session.query(ObservationFloat).count() == 1

    rv = api_client.get(f"/observations/")
    assert rv.status_code == 200
    response_content_1 = json.loads(rv.data)['data'][0]
    response_content_2 = json.loads(rv.data)['data'][1]
    response_content_3 = json.loads(rv.data)['data'][2]
    response_content_4 = json.loads(rv.data)['data'][3]
    assert_observations(response_content_1, observation_1.__dict__)
    assert_observations(response_content_2, observation_2.__dict__)
    assert_observations(response_content_3, observation_3.__dict__)
    assert_observations(response_content_4, observation_4.__dict__)


@pytest.mark.parametrize("test_input", [
    (["SensorA", True, "2020-03-18T12:00:00+00:00"])
])
def test_get_observation(api_client, orm_client, create_sensor_a,
                         test_input):
    assert orm_client.session.query(Observation).count() == 0
    assert orm_client.session.query(ObservationBoolean).count() == 0
    assert orm_client.session.query(ObservationString).count() == 0
    assert orm_client.session.query(ObservationInteger).count() == 0
    assert orm_client.session.query(ObservationFloat).count() == 0
    observation_1 = ObservationBooleanFactory2DB(sensor_name=test_input[0],
                                                 value=test_input[1],
                                                 time_start=test_input[2])
    assert orm_client.session.query(Observation).count() == 1
    assert orm_client.session.query(ObservationBoolean).count() == 1
    assert orm_client.session.query(ObservationString).count() == 0
    assert orm_client.session.query(ObservationInteger).count() == 0
    assert orm_client.session.query(ObservationFloat).count() == 0

    rv = api_client.get(f"/observations/{observation_1.id}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_observations(response_content, observation_1.__dict__)


@pytest.mark.parametrize("test_input, test_input_2, test_input_3, test_input_4", [
    (["SensorA", "True", "2020-03-18T12:00:00+00:00"],
     ["SensorB", "SAMPLEVALUE", "2020-03-18T12:00:00+00:00"],
     ["SensorC", "1", "2020-03-18T12:00:00+00:00"],
     ["SensorD", "0.2", "2020-03-18T12:02:00+00:00"])
])
def test_add_observation(api_client, orm_client, create_sensor_a, create_sensor_b,
                         create_sensor_c, create_sensor_d,
                         test_input, test_input_2, test_input_3, test_input_4):
    assert orm_client.session.query(Observation).count() == 0
    observation_1 = ObservationBooleanDictFactory(sensor_name=test_input[0],
                                                  value=test_input[1],
                                                  time_start=test_input[2])
    observation_2 = ObservationStringDictFactory(sensor_name=test_input_2[0],
                                                 value=test_input_2[1],
                                                 time_start=test_input_2[2])
    observation_3 = ObservationIntegerDictFactory(sensor_name=test_input_3[0],
                                                  value=test_input_3[1],
                                                  time_start=test_input_3[2])
    observation_4 = ObservationFloatDictFactory(sensor_name=test_input_4[0],
                                                value=test_input_4[1],
                                                time_start=test_input_4[2])
    assert orm_client.session.query(Observation).count() == 0

    # Test observation 1
    rv = api_client.post("/observations/", json=observation_1)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)['data']['id']

    # TODO Change to orm_client.session.query...
    rv = api_client.get(f"/observations/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_observations(response_content, observation_1)

    # Test observation 2
    rv = api_client.post("/observations/", json=observation_2)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)['data']['id']

    # TODO Change to orm_client.session.query...
    rv = api_client.get(f"/observations/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_observations(response_content, observation_2)

    # Test observation 3
    rv = api_client.post("/observations/", json=observation_3)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)['data']['id']

    # TODO Change to orm_client.session.query...
    rv = api_client.get(f"/observations/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_observations(response_content, observation_3)

    # Test observation 4
    rv = api_client.post("/observations/", json=observation_4)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)['data']['id']

    # TODO Change to orm_client.session.query...
    rv = api_client.get(f"/observations/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_observations(response_content, observation_4)


@pytest.mark.parametrize("test_input", [
    (["SensorA", True, "2020-03-18T12:00:00+00:00"])
])
def test_delete_observation(api_client, orm_client, create_sensor_a,
                            test_input):
    assert orm_client.session.query(Observation).count() == 0
    observation_1 = ObservationBooleanFactory2DB(sensor_name=test_input[0],
                                                 value=test_input[1],
                                                 time_start=test_input[2])
    assert orm_client.session.query(Observation).count() == 1

    rv = api_client.delete(f"/observations/{observation_1.id}")
    assert rv.status_code == 200

    assert orm_client.session.query(Observation).count() == 0
