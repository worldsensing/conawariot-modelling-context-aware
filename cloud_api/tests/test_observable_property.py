import pytest

from fixtures import ObservablePropertyFactory2DB, FeatureOfInterestFactory2DB
from models.ObservableProperty import ObservableValueTypeEnum


@pytest.fixture
def create_feature_of_interest():
    return FeatureOfInterestFactory2DB(name="Person")


@pytest.mark.parametrize("test_input, test_output", [
    (["Light1", "BOOLEAN", "Person"],
     ["0, Light1, BOOLEAN, Person, []"])
])
def test_observable_property_to_string(api_client, orm_client, create_feature_of_interest,
                                       test_input, test_output):
    observable_property = ObservablePropertyFactory2DB(
        name=test_input[0],
        value_type_to_measure=ObservableValueTypeEnum(test_input[1]),
        feature_of_interest_name=test_input[2])

    assert observable_property.__str__() == test_output[0]
