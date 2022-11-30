import json

import pytest

from fixtures import FeatureOfInterestFactory2DB, ActuatablePropertyDictFactory, \
    ObservablePropertyFactory2DB, ObservablePropertyDictFactory
from models import ObservableProperty
from models.ObservableProperty import ObservableValueTypeEnum


def assert_observable_properties(observable_property_api, observable_property_db):
    # assert observable_property_db["id"] == observable_property_api["id"]
    assert observable_property_db["name"] == observable_property_api["name"]
    if type(observable_property_db["value_type_to_measure"]) == ObservableValueTypeEnum:
        assert observable_property_db["value_type_to_measure"].value == \
               observable_property_api["value_type_to_measure"]
    else:
        assert observable_property_db["value_type_to_measure"] == \
               observable_property_api["value_type_to_measure"]
    assert observable_property_db["feature_of_interest_name"] == \
           observable_property_api["feature_of_interest_name"]


@pytest.fixture
def create_feature_of_interest():
    return FeatureOfInterestFactory2DB(name="Person")


@pytest.fixture
def create_feature_of_interest_2():
    return FeatureOfInterestFactory2DB(name="Cat")


@pytest.mark.parametrize("test_input, test_input_2", [
    (["arm_up", "BOOLEAN", "Person"],
     ["tail_down", "BOOLEAN", "Cat"])
])
def test_get_observable_property_all(api_client, orm_client, create_feature_of_interest,
                                     create_feature_of_interest_2,
                                     test_input, test_input_2):
    assert orm_client.session.query(ObservableProperty).count() == 0
    observable_property_1 = ObservablePropertyFactory2DB(
        name=test_input[0],
        value_type_to_measure=ObservableValueTypeEnum(test_input[1]),
        feature_of_interest_name=test_input[2])
    assert orm_client.session.query(ObservableProperty).count() == 1
    observable_property_2 = ObservablePropertyFactory2DB(
        name=test_input_2[0],
        value_type_to_measure=ObservableValueTypeEnum(test_input_2[1]),
        feature_of_interest_name=test_input_2[2])
    assert orm_client.session.query(ObservableProperty).count() == 2

    rv = api_client.get(f"/observable-properties/")
    assert rv.status_code == 200
    response_content_1 = json.loads(rv.data)['data'][0]
    response_content_2 = json.loads(rv.data)['data'][1]
    assert_observable_properties(response_content_1, observable_property_1.__dict__)
    assert_observable_properties(response_content_2, observable_property_2.__dict__)


@pytest.mark.parametrize("test_input", [
    (["arm_up", "BOOLEAN", "Person"])
])
def test_get_observable_property(api_client, orm_client, create_feature_of_interest,
                                 test_input):
    assert orm_client.session.query(ObservableProperty).count() == 0
    observable_property_1 = ObservablePropertyFactory2DB(
        name=test_input[0],
        value_type_to_measure=ObservableValueTypeEnum(test_input[1]),
        feature_of_interest_name=test_input[2])
    assert orm_client.session.query(ObservableProperty).count() == 1

    rv = api_client.get(f"/observable-properties/{observable_property_1.name}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_observable_properties(response_content, observable_property_1.__dict__)


@pytest.mark.parametrize("test_input", [
    (["arm_up", "BOOLEAN", "Person"])
])
def test_add_observable_property(api_client, orm_client, create_feature_of_interest,
                                 test_input):
    assert orm_client.session.query(ObservableProperty).count() == 0
    observable_property_1 = ObservablePropertyDictFactory(
        name=test_input[0],
        value_type_to_measure=test_input[1],
        feature_of_interest_name=test_input[2])
    assert orm_client.session.query(ObservableProperty).count() == 0

    rv = api_client.post("/observable-properties/", json=observable_property_1)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)['data']['name']
    assert response_content == observable_property_1["name"]

    # TODO Change to orm_client.session.query...
    rv = api_client.get(f"/observable-properties/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_observable_properties(response_content, observable_property_1)


@pytest.mark.parametrize("test_input, test_modify", [
    (["arm_up", "BOOLEAN", "Person"],
     ["arm_up", "STRING", "Person"])
])
def test_update_observable_property(api_client, orm_client, create_feature_of_interest,
                                    test_input, test_modify):
    assert orm_client.session.query(ObservableProperty).count() == 0
    observable_property_1 = ObservablePropertyFactory2DB(
        name=test_input[0],
        value_type_to_measure=ObservableValueTypeEnum(test_input[1]),
        feature_of_interest_name=test_input[2])
    assert orm_client.session.query(ObservableProperty).count() == 1

    observable_property_to_modify = ActuatablePropertyDictFactory(
        name=test_modify[0],
        value_type_to_measure=test_modify[1],
        feature_of_interest_name=test_modify[2])

    rv = api_client.put(f"/observable-properties/{observable_property_1.name}",
                        json=observable_property_to_modify)
    assert rv.status_code == 200
    assert orm_client.session.query(ObservableProperty).count() == 1

    rv = api_client.get(f"/observable-properties/{observable_property_1.name}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_observable_properties(response_content, observable_property_to_modify)


@pytest.mark.parametrize("test_input", [
    (["arm_up", "BOOLEAN", "Person"])
])
def test_delete_observable_property(api_client, orm_client, create_feature_of_interest,
                                    test_input):
    assert orm_client.session.query(ObservableProperty).count() == 0
    observable_property_1 = ObservablePropertyFactory2DB(
        name=test_input[0],
        value_type_to_measure=ObservableValueTypeEnum(test_input[1]),
        feature_of_interest_name=test_input[2])
    assert orm_client.session.query(ObservableProperty).count() == 1

    rv = api_client.delete(f"/observable-properties/{observable_property_1.name}")
    assert rv.status_code == 200

    assert orm_client.session.query(ObservableProperty).count() == 0
