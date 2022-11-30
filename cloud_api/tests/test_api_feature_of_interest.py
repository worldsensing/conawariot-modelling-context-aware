import json

import pytest

from fixtures import FeatureOfInterestFactory2DB, FeatureOfInterestDictFactory, LocationFactory2DB
from models import FeatureOfInterest


def assert_features_of_interest(feature_of_interest_api, feature_of_interest_db):
    # assert feature_of_interest_db["id"] == feature_of_interest_api["id"]
    assert feature_of_interest_db["name"] == feature_of_interest_api["name"]
    assert feature_of_interest_db["location_name"] == feature_of_interest_api["location_name"]


@pytest.fixture
def create_location():
    return LocationFactory2DB(name="MyLocation1")


@pytest.fixture
def create_location_2():
    return LocationFactory2DB(name="MyLocation2")


@pytest.mark.parametrize("test_input, test_input_2", [
    (["Person", "MyLocation1"],
     ["Cat", None])
])
def test_get_feature_of_interests_all(api_client, orm_client, create_location,
                                      test_input, test_input_2):
    assert orm_client.session.query(FeatureOfInterest).count() == 0
    feature_of_interest_1 = FeatureOfInterestFactory2DB(name=test_input[0],
                                                        location_name=test_input[1])
    assert orm_client.session.query(FeatureOfInterest).count() == 1
    feature_of_interest_2 = FeatureOfInterestFactory2DB(name=test_input_2[0],
                                                        location_name=test_input_2[1])
    assert orm_client.session.query(FeatureOfInterest).count() == 2

    rv = api_client.get(f"/features-of-interest/")
    assert rv.status_code == 200
    response_content_1 = json.loads(rv.data)['data'][0]
    response_content_2 = json.loads(rv.data)['data'][1]
    assert_features_of_interest(response_content_1, feature_of_interest_1.__dict__)
    assert_features_of_interest(response_content_2, feature_of_interest_2.__dict__)


@pytest.mark.parametrize("test_input", [
    (["Person", None])
])
def test_get_feature_of_interest(api_client, orm_client, create_location,
                                 test_input):
    assert orm_client.session.query(FeatureOfInterest).count() == 0
    feature_of_interest_1 = FeatureOfInterestFactory2DB(name=test_input[0],
                                                        location_name=test_input[1])
    assert orm_client.session.query(FeatureOfInterest).count() == 1

    rv = api_client.get(f"/features-of-interest/{feature_of_interest_1.name}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_features_of_interest(response_content, feature_of_interest_1.__dict__)


@pytest.mark.parametrize("test_input", [
    (["Person", "MyLocation1"])
])
def test_add_feature_of_interest(api_client, orm_client, create_location,
                                 test_input):
    assert orm_client.session.query(FeatureOfInterest).count() == 0
    feature_of_interest_1 = FeatureOfInterestDictFactory(name=test_input[0],
                                                         location_name=test_input[1])
    assert orm_client.session.query(FeatureOfInterest).count() == 0

    rv = api_client.post("/features-of-interest/", json=feature_of_interest_1)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)['data']['name']
    assert response_content == feature_of_interest_1["name"]

    # TODO Change to orm_client.session.query...
    rv = api_client.get(f"/features-of-interest/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_features_of_interest(response_content, feature_of_interest_1)


@pytest.mark.parametrize("test_input, test_modify", [
    (["Person", "MyLocation1"],
     ["Person", "MyLocation2"])
])
def test_update_feature_of_interest(api_client, orm_client, create_location, create_location_2,
                                    test_input, test_modify):
    assert orm_client.session.query(FeatureOfInterest).count() == 0
    feature_of_interest_1 = FeatureOfInterestFactory2DB(name=test_input[0],
                                                        location_name=test_input[1])
    assert orm_client.session.query(FeatureOfInterest).count() == 1

    feature_of_interest_to_modify = FeatureOfInterestDictFactory(name=test_modify[0],
                                                                 location_name=test_modify[1])

    rv = api_client.put(f"/features-of-interest/{feature_of_interest_1.name}",
                        json=feature_of_interest_to_modify)
    assert rv.status_code == 200
    assert orm_client.session.query(FeatureOfInterest).count() == 1

    rv = api_client.get(f"/features-of-interest/{feature_of_interest_1.name}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_features_of_interest(response_content, feature_of_interest_to_modify)


@pytest.mark.parametrize("test_input", [
    (["Person", "MyLocation1"])
])
def test_delete_feature_of_interest(api_client, orm_client, create_location,
                                    test_input):
    assert orm_client.session.query(FeatureOfInterest).count() == 0
    feature_of_interest_1 = FeatureOfInterestFactory2DB(name=test_input[0],
                                                        location_name=test_input[1])
    assert orm_client.session.query(FeatureOfInterest).count() == 1

    rv = api_client.delete(f"/features-of-interest/{feature_of_interest_1.name}")
    assert rv.status_code == 200

    assert orm_client.session.query(FeatureOfInterest).count() == 0
