import json

import pytest

from fixtures import LocationFactory2DB, LocationDictFactory
from models import Location


def assert_locations(location_api, location_db):
    # assert location_db["id"] == location_api["id"]
    assert location_db["name"] == location_api["name"]
    assert location_db["latlng"] == location_api["latlng"]


@pytest.mark.parametrize("test_input, test_input_2", [
    (["MyLocation1", "41.2, 2.1"],
     ["MyLocation2", None])
])
def test_get_locations_all(api_client, orm_client,
                           test_input, test_input_2):
    assert orm_client.session.query(Location).count() == 0
    location_1 = LocationFactory2DB(name=test_input[0],
                                    latlng=test_input[1])
    assert orm_client.session.query(Location).count() == 1
    location_2 = LocationFactory2DB(name=test_input_2[0],
                                    latlng=test_input_2[1])
    assert orm_client.session.query(Location).count() == 2

    rv = api_client.get(f"/locations/")
    assert rv.status_code == 200
    response_content_1 = json.loads(rv.data)['data'][0]
    response_content_2 = json.loads(rv.data)['data'][1]
    assert_locations(response_content_1, location_1.__dict__)
    assert_locations(response_content_2, location_2.__dict__)


@pytest.mark.parametrize("test_input", [
    (["MyLocation1", "41.2, 2.1"])
])
def test_get_location(api_client, orm_client,
                      test_input):
    assert orm_client.session.query(Location).count() == 0
    location_1 = LocationFactory2DB(name=test_input[0],
                                    latlng=test_input[1])
    assert orm_client.session.query(Location).count() == 1

    rv = api_client.get(f"/locations/{location_1.name}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_locations(response_content, location_1.__dict__)


@pytest.mark.parametrize("test_input", [
    (["MyLocation1", "41.2, 2.1"])
])
def test_add_location(api_client, orm_client,
                      test_input):
    assert orm_client.session.query(Location).count() == 0
    location_1 = LocationDictFactory(name=test_input[0],
                                     latlng=test_input[1])
    assert orm_client.session.query(Location).count() == 0

    rv = api_client.post("/locations/", json=location_1)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)['data']['name']
    assert response_content == location_1["name"]

    # TODO Change to orm_client.session.query...
    rv = api_client.get(f"/locations/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_locations(response_content, location_1)


@pytest.mark.parametrize("test_input, test_modify", [
    (["MyLocation1", "41.2, 2.1"],
     ["MyLocation1", "41.2, 2.2"])
])
def test_update_location(api_client, orm_client,
                         test_input, test_modify):
    assert orm_client.session.query(Location).count() == 0
    location_1 = LocationFactory2DB(name=test_input[0],
                                    latlng=test_input[1])
    assert orm_client.session.query(Location).count() == 1

    location_to_modify = LocationDictFactory(name=test_modify[0],
                                             latlng=test_modify[1])

    rv = api_client.put(f"/locations/{location_1.name}",
                        json=location_to_modify)
    assert rv.status_code == 200
    assert orm_client.session.query(Location).count() == 1

    rv = api_client.get(f"/locations/{location_1.name}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_locations(response_content, location_to_modify)


@pytest.mark.parametrize("test_input", [
    (["MyLocation1", "41.2, 2.1"])
])
def test_delete_location(api_client, orm_client,
                         test_input):
    assert orm_client.session.query(Location).count() == 0
    location_1 = LocationFactory2DB(name=test_input[0],
                                    latlng=test_input[1])
    assert orm_client.session.query(Location).count() == 1

    rv = api_client.delete(f"/locations/{location_1.name}")
    assert rv.status_code == 200

    assert orm_client.session.query(Location).count() == 0
