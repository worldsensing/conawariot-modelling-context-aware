import json

import pytest

from fixtures import PlatformFactory2DB, PlatformDictFactory, LocationFactory2DB
from models import Platform


def assert_platforms(platform_api, platform_db):
    # assert feature_of_interest_db["id"] == feature_of_interest_api["id"]
    assert platform_db["name"] == platform_api["name"]
    assert platform_db["location_name"] == platform_api["location_name"]


@pytest.fixture
def create_location():
    return LocationFactory2DB(name="MyLocation1")


@pytest.fixture
def create_location_2():
    return LocationFactory2DB(name="MyLocation2")


@pytest.mark.parametrize("test_input, test_input_2", [
    (["Car", "MyLocation1"],
     ["Site", None])
])
def test_get_platform_all(api_client, orm_client, create_location,
                          test_input, test_input_2):
    assert orm_client.session.query(Platform).count() == 0
    platform_1 = PlatformFactory2DB(name=test_input[0],
                                    location_name=test_input[1])
    assert orm_client.session.query(Platform).count() == 1
    platform_2 = PlatformFactory2DB(name=test_input_2[0],
                                    location_name=test_input_2[1])
    assert orm_client.session.query(Platform).count() == 2

    rv = api_client.get(f"/platforms/")
    assert rv.status_code == 200
    response_content_1 = json.loads(rv.data)['data'][0]
    response_content_2 = json.loads(rv.data)['data'][1]
    assert_platforms(response_content_1, platform_1.__dict__)
    assert_platforms(response_content_2, platform_2.__dict__)


@pytest.mark.parametrize("test_input", [
    (["Site", None])
])
def test_get_platform(api_client, orm_client, create_location,
                      test_input):
    assert orm_client.session.query(Platform).count() == 0
    platform_1 = PlatformFactory2DB(name=test_input[0],
                                    location_name=test_input[1])
    assert orm_client.session.query(Platform).count() == 1

    rv = api_client.get(f"/platforms/{platform_1.name}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_platforms(response_content, platform_1.__dict__)


@pytest.mark.parametrize("test_input", [
    (["Car", "MyLocation1"])
])
def test_add_platform(api_client, orm_client, create_location,
                      test_input):
    assert orm_client.session.query(Platform).count() == 0
    platform_1 = PlatformDictFactory(name=test_input[0],
                                     location_name=test_input[1])
    assert orm_client.session.query(Platform).count() == 0

    rv = api_client.post("/platforms/", json=platform_1)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)['data']['name']
    assert response_content == platform_1["name"]

    # TODO Change to orm_client.session.query...
    rv = api_client.get(f"/platforms/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_platforms(response_content, platform_1)


@pytest.mark.parametrize("test_input, test_modify", [
    (["Car", "MyLocation1"],
     ["Car", "MyLocation2"])
])
def test_update_platform(api_client, orm_client, create_location, create_location_2,
                         test_input, test_modify):
    assert orm_client.session.query(Platform).count() == 0
    platform_1 = PlatformFactory2DB(name=test_input[0],
                                    location_name=test_input[1])
    assert orm_client.session.query(Platform).count() == 1

    platform_to_modify = PlatformDictFactory(name=test_modify[0],
                                             location_name=test_modify[1])

    rv = api_client.put(f"/platforms/{platform_1.name}",
                        json=platform_to_modify)
    assert rv.status_code == 200
    assert orm_client.session.query(Platform).count() == 1

    rv = api_client.get(f"/platforms/{platform_1.name}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_platforms(response_content, platform_to_modify)


@pytest.mark.parametrize("test_input", [
    (["Car", "MyLocation1"])
])
def test_delete_platform(api_client, orm_client, create_location,
                         test_input):
    assert orm_client.session.query(Platform).count() == 0
    platform_1 = PlatformFactory2DB(name=test_input[0],
                                    location_name=test_input[1])
    assert orm_client.session.query(Platform).count() == 1

    rv = api_client.delete(f"/platforms/{platform_1.name}")
    assert rv.status_code == 200

    assert orm_client.session.query(Platform).count() == 0
