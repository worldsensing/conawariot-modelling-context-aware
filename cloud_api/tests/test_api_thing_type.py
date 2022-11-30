import json

import pytest

from fixtures import ThingTypeFactory2DB, ThingTypeDictFactory
from models import ThingType


def assert_thing_types(thing_type_api, thing_type_db):
    # assert thing_db["id"] == thing_api["id"]
    assert thing_type_db["name"] == thing_type_api["name"]


@pytest.mark.parametrize("test_input, test_input_2", [
    (["Inclinometer"],
     ["Accelerometer"])
])
def test_get_thing_types_all(api_client, orm_client,
                             test_input, test_input_2):
    assert orm_client.session.query(ThingType).count() == 0
    thing_type_1 = ThingTypeFactory2DB(name=test_input[0])
    assert orm_client.session.query(ThingType).count() == 1
    thing_type_2 = ThingTypeFactory2DB(name=test_input_2[0])
    assert orm_client.session.query(ThingType).count() == 2

    rv = api_client.get(f"/thing-types/")
    assert rv.status_code == 200
    response_content_1 = json.loads(rv.data)["data"][0]
    response_content_2 = json.loads(rv.data)["data"][1]
    assert_thing_types(response_content_1, thing_type_1.__dict__)
    assert_thing_types(response_content_2, thing_type_2.__dict__)


@pytest.mark.parametrize("test_input", [
    (["Inclinometer"])
])
def test_get_thing_type(api_client, orm_client,
                        test_input):
    assert orm_client.session.query(ThingType).count() == 0
    thing_type_1 = ThingTypeFactory2DB(name=test_input[0])
    assert orm_client.session.query(ThingType).count() == 1

    rv = api_client.get(f"/thing-types/{thing_type_1.name}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)["data"]
    assert_thing_types(response_content, thing_type_1.__dict__)


@pytest.mark.parametrize("test_input", [
    (["Inclinometer"])
])
def test_add_thing_type(api_client, orm_client,
                        test_input):
    assert orm_client.session.query(ThingType).count() == 0
    thing_type_1 = ThingTypeDictFactory(name=test_input[0])
    assert orm_client.session.query(ThingType).count() == 0

    rv = api_client.post("/thing-types/", json=thing_type_1)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)["data"]["name"]
    assert response_content == thing_type_1["name"]

    # TODO Change to orm_client.session.query...
    rv = api_client.get(f"/thing-types/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)["data"]
    assert_thing_types(response_content, thing_type_1)


@pytest.mark.parametrize("test_input, test_modify", [
    (["Inclinometer"],
     ["Inclinometer"])
])
def test_update_thing(api_client, orm_client,
                      test_input, test_modify):
    assert orm_client.session.query(ThingType).count() == 0
    thing_type_1 = ThingTypeFactory2DB(name=test_input[0])
    assert orm_client.session.query(ThingType).count() == 1

    thing_type_to_modify = ThingTypeDictFactory(name=test_modify[0])

    rv = api_client.put(f"/thing-types/{thing_type_1.name}",
                        json=thing_type_to_modify)
    assert rv.status_code == 200
    assert orm_client.session.query(ThingType).count() == 1

    rv = api_client.get(f"/thing-types/{thing_type_1.name}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)["data"]
    assert_thing_types(response_content, thing_type_to_modify)


@pytest.mark.parametrize("test_input", [
    (["Inclinometer"])
])
def test_delete_thing_type(api_client, orm_client,
                           test_input):
    assert orm_client.session.query(ThingType).count() == 0
    thing_type_1 = ThingTypeFactory2DB(name=test_input[0])
    assert orm_client.session.query(ThingType).count() == 1

    rv = api_client.delete(f"/thing-types/{thing_type_1.name}")
    assert rv.status_code == 200

    assert orm_client.session.query(ThingType).count() == 0
