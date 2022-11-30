import json

import pytest

from fixtures import FeatureOfInterestFactory2DB, ActuatablePropertyFactory2DB, \
    ActuatablePropertyDictFactory
from models import ActuatableProperty


def assert_actuatable_properties(actuatable_property_api, actuatable_property_db):
    # assert actuatable_property_db["id"] == actuatable_property_api["id"]
    assert actuatable_property_db["name"] == actuatable_property_api["name"]
    assert actuatable_property_db["feature_of_interest_name"] == \
           actuatable_property_api["feature_of_interest_name"]


@pytest.fixture
def create_feature_of_interest():
    return FeatureOfInterestFactory2DB(name="Person")


@pytest.fixture
def create_feature_of_interest_2():
    return FeatureOfInterestFactory2DB(name="Cat")


@pytest.mark.parametrize("test_input, test_input_2", [
    (["Arm", "Person"],
     ["Tail", "Cat"])
])
def test_get_actuatable_property_all(api_client, orm_client, create_feature_of_interest,
                                     create_feature_of_interest_2,
                                     test_input, test_input_2):
    assert orm_client.session.query(ActuatableProperty).count() == 0
    actuatable_property_1 = ActuatablePropertyFactory2DB(name=test_input[0],
                                                         feature_of_interest_name=test_input[1])
    assert orm_client.session.query(ActuatableProperty).count() == 1
    actuatable_property_2 = ActuatablePropertyFactory2DB(name=test_input_2[0],
                                                         feature_of_interest_name=test_input_2[1])
    assert orm_client.session.query(ActuatableProperty).count() == 2

    rv = api_client.get(f"/actuatable-properties/")
    assert rv.status_code == 200
    response_content_1 = json.loads(rv.data)['data'][0]
    response_content_2 = json.loads(rv.data)['data'][1]
    assert_actuatable_properties(response_content_1, actuatable_property_1.__dict__)
    assert_actuatable_properties(response_content_2, actuatable_property_2.__dict__)


@pytest.mark.parametrize("test_input", [
    (["Leg", "Person"])
])
def test_get_actuatable_property(api_client, orm_client, create_feature_of_interest,
                                 test_input):
    assert orm_client.session.query(ActuatableProperty).count() == 0
    actuatable_property_1 = ActuatablePropertyFactory2DB(name=test_input[0],
                                                         feature_of_interest_name=test_input[1])
    assert orm_client.session.query(ActuatableProperty).count() == 1

    rv = api_client.get(f"/actuatable-properties/{actuatable_property_1.name}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_actuatable_properties(response_content, actuatable_property_1.__dict__)


@pytest.mark.parametrize("test_input", [
    (["Leg", "Person"])
])
def test_add_actuatable_property(api_client, orm_client, create_feature_of_interest,
                                 test_input):
    assert orm_client.session.query(ActuatableProperty).count() == 0
    actuatable_property_1 = ActuatablePropertyDictFactory(name=test_input[0],
                                                          feature_of_interest_name=test_input[1])
    assert orm_client.session.query(ActuatableProperty).count() == 0

    rv = api_client.post("/actuatable-properties/", json=actuatable_property_1)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)['data']['name']
    assert response_content == actuatable_property_1["name"]

    # TODO Change to orm_client.session.query...
    rv = api_client.get(f"/actuatable-properties/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_actuatable_properties(response_content, actuatable_property_1)


@pytest.mark.parametrize("test_input, test_modify", [
    (["Leg", "Person"],
     ["Leg2", "Person"])
])
def test_update_actuatable_property(api_client, orm_client, create_feature_of_interest,
                                    test_input, test_modify):
    assert orm_client.session.query(ActuatableProperty).count() == 0
    actuatable_property_1 = ActuatablePropertyFactory2DB(name=test_input[0],
                                                         feature_of_interest_name=test_input[1])
    assert orm_client.session.query(ActuatableProperty).count() == 1

    actuatable_property_to_modify = ActuatablePropertyDictFactory(
        name=test_modify[0],
        feature_of_interest_name=test_modify[1])

    rv = api_client.put(f"/actuatable-properties/{actuatable_property_1.name}",
                        json=actuatable_property_to_modify)
    assert rv.status_code == 200
    assert orm_client.session.query(ActuatableProperty).count() == 1

    rv = api_client.get(f"/actuatable-properties/{actuatable_property_1.name}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_actuatable_properties(response_content, actuatable_property_to_modify)


@pytest.mark.parametrize("test_input", [
    (["Leg", "Person"])
])
def test_delete_actuatable_property(api_client, orm_client, create_feature_of_interest,
                                    test_input):
    assert orm_client.session.query(ActuatableProperty).count() == 0
    actuatable_property_1 = ActuatablePropertyFactory2DB(name=test_input[0],
                                                         feature_of_interest_name=test_input[1])
    assert orm_client.session.query(ActuatableProperty).count() == 1

    rv = api_client.delete(f"/actuatable-properties/{actuatable_property_1.name}")
    assert rv.status_code == 200

    assert orm_client.session.query(ActuatableProperty).count() == 0
