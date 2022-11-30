import json

import pytest

from fixtures import ActuatorFactory2DB, ActuatorDictFactory, ThingTypeFactory2DB, \
    LocationFactory2DB, ThingFactory2DB, FeatureOfInterestFactory2DB, ActuatablePropertyFactory2DB
from models import Actuator


@pytest.fixture
def create_location_2():
    return LocationFactory2DB(name="MyLocation2")


@pytest.fixture
def create_location():
    return LocationFactory2DB(name="MyLocation1")


@pytest.fixture
def create_feature_of_interest():
    return FeatureOfInterestFactory2DB(name="Car")


@pytest.fixture
def create_actuatable_property_2(create_feature_of_interest):
    return ActuatablePropertyFactory2DB(name="TempActuator", feature_of_interest_name="Car")


@pytest.fixture
def create_actuatable_property(create_feature_of_interest):
    return ActuatablePropertyFactory2DB(name="WindShieldActuator",
                                        feature_of_interest_name="Car")


@pytest.fixture
def create_thing_type():
    return ThingTypeFactory2DB(name="RainModule")


@pytest.fixture
def create_thing(create_thing_type):
    return ThingFactory2DB(name="Raspberry1", type_name="RainModule")


def assert_actuators(actuator_api, actuator_db):
    # assert actuator_db["id"] == actuator_api["id"]
    assert actuator_db["name"] == actuator_api["name"]
    assert actuator_db["thing_name"] == actuator_api["thing_name"]
    assert actuator_db["actuatable_property_name"] == actuator_api["actuatable_property_name"]
    assert actuator_db["location_name"] == actuator_api["location_name"]


@pytest.mark.parametrize("test_input, test_input_2", [
    (["RainActuator", "Raspberry1", "WindShieldActuator", "MyLocation1"],
     ["TemperatureActuator", "Raspberry1", "TempActuator", None])
])
def test_get_actuators_all(api_client, orm_client, create_thing, create_actuatable_property,
                           create_actuatable_property_2, create_location,
                           test_input, test_input_2):
    assert orm_client.session.query(Actuator).count() == 0
    actuator_1 = ActuatorFactory2DB(name=test_input[0],
                                    thing_name=test_input[1],
                                    actuatable_property_name=test_input[2],
                                    location_name=test_input[3])
    assert orm_client.session.query(Actuator).count() == 1
    actuator_2 = ActuatorFactory2DB(name=test_input_2[0],
                                    thing_name=test_input_2[1],
                                    actuatable_property_name=test_input_2[2],
                                    location_name=test_input_2[3])
    assert orm_client.session.query(Actuator).count() == 2

    rv = api_client.get(f"/actuators/")
    assert rv.status_code == 200
    response_content_1 = json.loads(rv.data)['data'][0]
    response_content_2 = json.loads(rv.data)['data'][1]
    assert_actuators(response_content_1, actuator_1.__dict__)
    assert_actuators(response_content_2, actuator_2.__dict__)


@pytest.mark.parametrize("test_input", [
    (["RainActuator", "Raspberry1", "WindShieldActuator", "MyLocation1"])
])
def test_get_actuator(api_client, orm_client, create_thing, create_actuatable_property,
                      create_location,
                      test_input):
    assert orm_client.session.query(Actuator).count() == 0
    actuator_1 = ActuatorFactory2DB(name=test_input[0],
                                    thing_name=test_input[1],
                                    actuatable_property_name=test_input[2],
                                    location_name=test_input[3])
    assert orm_client.session.query(Actuator).count() == 1

    rv = api_client.get(f"/actuators/{actuator_1.name}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_actuators(response_content, actuator_1.__dict__)


@pytest.mark.parametrize("test_input", [
    (["RainActuator", "Raspberry1", "WindShieldActuator", "MyLocation1"]),
    (["TemperatureActuator", "Raspberry1", "TempActuator", None])
])
def test_add_actuator(api_client, orm_client, create_thing, create_actuatable_property,
                      create_actuatable_property_2, create_location,
                      test_input):
    assert orm_client.session.query(Actuator).count() == 0
    actuator_1 = ActuatorDictFactory(name=test_input[0],
                                     thing_name=test_input[1],
                                     actuatable_property_name=test_input[2],
                                     location_name=test_input[3])
    assert orm_client.session.query(Actuator).count() == 0

    rv = api_client.post("/actuators/", json=actuator_1)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)['data']['name']
    assert response_content == actuator_1["name"]

    # TODO Change to orm_client.session.query...
    rv = api_client.get(f"/actuators/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_actuators(response_content, actuator_1)


@pytest.mark.parametrize("test_input, test_modify", [
    (["RainActuator", "Raspberry1", "WindShieldActuator", "MyLocation1"],
     ["RainActuator", "Raspberry1", "WindShieldActuator", "MyLocation2"])
])
def test_update_actuator(api_client, orm_client, create_thing, create_actuatable_property,
                         create_location, create_location_2,
                         test_input, test_modify):
    assert orm_client.session.query(Actuator).count() == 0
    actuator_1 = ActuatorFactory2DB(name=test_input[0],
                                    thing_name=test_input[1],
                                    actuatable_property_name=test_input[2],
                                    location_name=test_input[3])
    assert orm_client.session.query(Actuator).count() == 1

    actuator_to_modify = ActuatorDictFactory(name=test_input[0],
                                             thing_name=test_modify[1],
                                             actuatable_property_name=test_modify[2],
                                             location_name=test_modify[3])

    rv = api_client.put(f"/actuators/{actuator_1.name}",
                        json=actuator_to_modify)
    assert rv.status_code == 200
    assert orm_client.session.query(Actuator).count() == 1

    rv = api_client.get(f"/actuators/{actuator_1.name}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_actuators(response_content, actuator_to_modify)


@pytest.mark.parametrize("test_input", [
    (["RainActuator", "Raspberry1", "WindShieldActuator", "MyLocation1"])
])
def test_delete_actuator(api_client, orm_client, create_thing, create_actuatable_property,
                         create_location,
                         test_input):
    assert orm_client.session.query(Actuator).count() == 0
    actuator_1 = ActuatorFactory2DB(name=test_input[0],
                                    thing_name=test_input[1],
                                    actuatable_property_name=test_input[2],
                                    location_name=test_input[3])
    assert orm_client.session.query(Actuator).count() == 1

    rv = api_client.delete(f"/actuators/{actuator_1.name}")
    assert rv.status_code == 200

    assert orm_client.session.query(Actuator).count() == 0
