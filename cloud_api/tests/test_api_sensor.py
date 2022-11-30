import json

import pytest

from fixtures import SensorFactory2DB, SensorDictFactory, ThingTypeFactory2DB, \
    LocationFactory2DB, ThingFactory2DB, FeatureOfInterestFactory2DB, ObservablePropertyFactory2DB
from models import Sensor
from models.ObservableProperty import ObservableValueTypeEnum


@pytest.fixture
def create_location_2():
    return LocationFactory2DB(name="MyLocation2")


@pytest.fixture
def create_location():
    return LocationFactory2DB(name="MyLocation1")


@pytest.fixture
def create_feature_of_interest():
    return FeatureOfInterestFactory2DB(name="Person")


@pytest.fixture
def create_observable_property_2(create_feature_of_interest):
    return ObservablePropertyFactory2DB(name="TempProp", feature_of_interest_name="Person",
                                        value_type_to_measure=ObservableValueTypeEnum.value_integer)


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


def assert_sensors(sensor_api, sensor_db):
    # assert sensor_db["id"] == sensor_api["id"]
    assert sensor_db["name"] == sensor_api["name"]
    assert sensor_db["thing_name"] == sensor_api["thing_name"]
    assert sensor_db["observable_property_name"] == sensor_api["observable_property_name"]
    assert sensor_db["location_name"] == sensor_api["location_name"]


@pytest.mark.parametrize("test_input, test_input_2", [
    (["RainSensor", "Raspberry1", "RainProp", "MyLocation1"],
     ["TemperatureSensor", "Raspberry1", "TempProp", None])
])
def test_get_sensors_all(api_client, orm_client, create_thing, create_observable_property,
                         create_observable_property_2, create_location,
                         test_input, test_input_2):
    assert orm_client.session.query(Sensor).count() == 0
    sensor_1 = SensorFactory2DB(name=test_input[0],
                                thing_name=test_input[1],
                                observable_property_name=test_input[2],
                                location_name=test_input[3])
    assert orm_client.session.query(Sensor).count() == 1
    sensor_2 = SensorFactory2DB(name=test_input_2[0],
                                thing_name=test_input_2[1],
                                observable_property_name=test_input_2[2],
                                location_name=test_input_2[3])
    assert orm_client.session.query(Sensor).count() == 2

    rv = api_client.get(f"/sensors/")
    assert rv.status_code == 200
    response_content_1 = json.loads(rv.data)['data'][0]
    response_content_2 = json.loads(rv.data)['data'][1]
    assert_sensors(response_content_1, sensor_1.__dict__)
    assert_sensors(response_content_2, sensor_2.__dict__)


@pytest.mark.parametrize("test_input", [
    (["RainSensor", "Raspberry1", "RainProp", "MyLocation1"])
])
def test_get_sensor(api_client, orm_client, create_thing, create_observable_property,
                    create_location,
                    test_input):
    assert orm_client.session.query(Sensor).count() == 0
    sensor_1 = SensorFactory2DB(name=test_input[0],
                                thing_name=test_input[1],
                                observable_property_name=test_input[2],
                                location_name=test_input[3])
    assert orm_client.session.query(Sensor).count() == 1

    rv = api_client.get(f"/sensors/{sensor_1.name}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_sensors(response_content, sensor_1.__dict__)


@pytest.mark.parametrize("test_input", [
    (["RainSensor", "Raspberry1", "RainProp", "MyLocation1"]),
    (["TemperatureSensor", "Raspberry1", "TempProp", None])
])
def test_add_sensor(api_client, orm_client, create_thing, create_observable_property,
                    create_observable_property_2, create_location,
                    test_input):
    assert orm_client.session.query(Sensor).count() == 0
    sensor_1 = SensorDictFactory(name=test_input[0],
                                 thing_name=test_input[1],
                                 observable_property_name=test_input[2],
                                 location_name=test_input[3])
    assert orm_client.session.query(Sensor).count() == 0

    rv = api_client.post("/sensors/", json=sensor_1)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)['data']['name']
    assert response_content == sensor_1["name"]

    # TODO Change to orm_client.session.query...
    rv = api_client.get(f"/sensors/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_sensors(response_content, sensor_1)


@pytest.mark.parametrize("test_input, test_modify", [
    (["RainSensor", "Raspberry1", "RainProp", "MyLocation1"],
     ["RainSensor", "Raspberry1", "RainProp", "MyLocation2"])
])
def test_update_sensor(api_client, orm_client, create_thing, create_observable_property,
                       create_location, create_location_2,
                       test_input, test_modify):
    assert orm_client.session.query(Sensor).count() == 0
    sensor_1 = SensorFactory2DB(name=test_input[0],
                                thing_name=test_input[1],
                                observable_property_name=test_input[2],
                                location_name=test_input[3])
    assert orm_client.session.query(Sensor).count() == 1

    sensor_to_modify = SensorDictFactory(name=test_input[0],
                                         thing_name=test_modify[1],
                                         observable_property_name=test_modify[2],
                                         location_name=test_modify[3])

    rv = api_client.put(f"/sensors/{sensor_1.name}",
                        json=sensor_to_modify)
    assert rv.status_code == 200
    assert orm_client.session.query(Sensor).count() == 1

    rv = api_client.get(f"/sensors/{sensor_1.name}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_sensors(response_content, sensor_to_modify)


@pytest.mark.parametrize("test_input", [
    (["RainSensor", "Raspberry1", "RainProp", "MyLocation1"])
])
def test_delete_sensor(api_client, orm_client, create_thing, create_observable_property,
                       create_location,
                       test_input):
    assert orm_client.session.query(Sensor).count() == 0
    sensor_1 = SensorFactory2DB(name=test_input[0],
                                thing_name=test_input[1],
                                observable_property_name=test_input[2],
                                location_name=test_input[3])
    assert orm_client.session.query(Sensor).count() == 1

    rv = api_client.delete(f"/sensors/{sensor_1.name}")
    assert rv.status_code == 200

    assert orm_client.session.query(Sensor).count() == 0
