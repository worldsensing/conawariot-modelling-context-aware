import json

import pytest

from fixtures import ThingFactory2DB, ThingDictFactory, ThingTypeFactory2DB, \
    LocationFactory2DB
from models import Thing


@pytest.fixture
def create_thing_type():
    return ThingTypeFactory2DB(name="Inclinometer")


@pytest.fixture
def create_location_2():
    return LocationFactory2DB(name="MyLocation2")


@pytest.fixture
def create_location():
    return LocationFactory2DB(name="MyLocation1")


def assert_things(thing_api, thing_db):
    # assert thing_db["id"] == thing_api["id"]
    assert thing_db["name"] == thing_api["name"]
    assert thing_db["type_name"] == thing_api["type_name"]
    assert thing_db["location_name"] == thing_api["location_name"]


@pytest.mark.parametrize("test_input, test_input_2", [
    (["Arduino", "Inclinometer", "MyLocation1"],
     ["Raspberry", "Inclinometer", "MyLocation1"])
])
def test_get_things_all(api_client, orm_client, create_thing_type, create_location,
                        test_input, test_input_2):
    assert orm_client.session.query(Thing).count() == 0
    thing_1 = ThingFactory2DB(name=test_input[0],
                              type_name=test_input[1],
                              location_name=test_input[2])
    assert orm_client.session.query(Thing).count() == 1
    thing_2 = ThingFactory2DB(name=test_input_2[0],
                              type_name=test_input_2[1],
                              location_name=test_input_2[2])
    assert orm_client.session.query(Thing).count() == 2

    rv = api_client.get(f"/things/")
    assert rv.status_code == 200
    response_content_1 = json.loads(rv.data)['data'][0]
    response_content_2 = json.loads(rv.data)['data'][1]
    assert_things(response_content_1, thing_1.__dict__)
    assert_things(response_content_2, thing_2.__dict__)


@pytest.mark.parametrize("test_input", [
    (["Arduino", "Inclinometer", "MyLocation1"])
])
def test_get_thing(api_client, orm_client, create_thing_type, create_location,
                   test_input):
    assert orm_client.session.query(Thing).count() == 0
    thing_1 = ThingFactory2DB(name=test_input[0],
                              type_name=test_input[1],
                              location_name=test_input[2])
    assert orm_client.session.query(Thing).count() == 1

    rv = api_client.get(f"/things/{thing_1.name}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_things(response_content, thing_1.__dict__)


@pytest.mark.parametrize("test_input", [
    (["Raspberry", "Inclinometer", "MyLocation1"]),
    (["Raspberry", "Inclinometer", None])
])
def test_add_thing(api_client, orm_client, create_thing_type, create_location,
                   test_input):
    assert orm_client.session.query(Thing).count() == 0
    thing_1 = ThingDictFactory(name=test_input[0],
                               type_name=test_input[1],
                               location_name=test_input[2])
    assert orm_client.session.query(Thing).count() == 0

    rv = api_client.post("/things/", json=thing_1)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)['data']['name']
    assert response_content == thing_1["name"]

    # TODO Change to orm_client.session.query...
    rv = api_client.get(f"/things/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_things(response_content, thing_1)


@pytest.mark.parametrize("test_input, test_modify", [
    (["Raspberry", "Inclinometer", "MyLocation1"],
     ["Raspberry", "Inclinometer", "MyLocation2"])
])
def test_update_thing(api_client, orm_client, create_thing_type, create_location, create_location_2,
                      test_input, test_modify):
    assert orm_client.session.query(Thing).count() == 0
    thing_1 = ThingFactory2DB(name=test_input[0],
                              type_name=test_input[1],
                              location_name=test_input[2])
    assert orm_client.session.query(Thing).count() == 1

    thing_to_modify = ThingDictFactory(name=test_input[0],
                                       type_name=test_input[1],
                                       location_name=test_input[2])

    rv = api_client.put(f"/things/{thing_1.name}",
                        json=thing_to_modify)
    assert rv.status_code == 200
    assert orm_client.session.query(Thing).count() == 1

    rv = api_client.get(f"/things/{thing_1.name}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_things(response_content, thing_to_modify)


@pytest.mark.parametrize("test_input", [
    (["Arduino", "Inclinometer", "MyLocation1"])
])
def test_delete_thing(api_client, orm_client, create_thing_type, create_location,
                      test_input):
    assert orm_client.session.query(Thing).count() == 0
    thing_1 = ThingFactory2DB(name=test_input[0],
                              type_name=test_input[1],
                              location_name=test_input[2])
    assert orm_client.session.query(Thing).count() == 1

    rv = api_client.delete(f"/things/{thing_1.name}")
    assert rv.status_code == 200

    assert orm_client.session.query(Thing).count() == 0
