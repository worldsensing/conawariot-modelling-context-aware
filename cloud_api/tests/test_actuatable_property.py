import pytest

from fixtures import ActuatablePropertyFactory2DB, FeatureOfInterestFactory2DB


@pytest.fixture
def create_feature_of_interest():
    return FeatureOfInterestFactory2DB(name="Person")


@pytest.mark.parametrize("test_input, test_output", [
    (["Leg1", "Person"],
     ["0, Leg1, Person, []"])
])
def test_actuatable_property_to_string(api_client, orm_client, create_feature_of_interest,
                                       test_input, test_output):
    actuatable_property = ActuatablePropertyFactory2DB(name=test_input[0],
                                                       feature_of_interest_name=test_input[1])

    assert actuatable_property.__str__() == test_output[0]
