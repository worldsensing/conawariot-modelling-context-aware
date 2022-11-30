import pytest

from fixtures import FeatureOfInterestFactory2DB, LocationFactory2DB


@pytest.fixture
def create_location():
    return LocationFactory2DB(name="MyLocation2")


@pytest.mark.parametrize("test_input, test_output", [
    (["Person", "MyLocation2"],
     ["0, Person, MyLocation2, [], []"])
])
def test_feature_of_interest_to_string(api_client, orm_client, create_location,
                                       test_input, test_output):
    feature_of_interest = FeatureOfInterestFactory2DB(name=test_input[0],
                                                      location_name=test_input[1])

    assert feature_of_interest.__str__() == test_output[0]


@pytest.mark.parametrize("test_input, test_output", [
    (["Person"],
     ["0, Person, None, [], []"])
])
def test_feature_of_interest_no_location_to_string(api_client, orm_client, create_location,
                                                   test_input, test_output):
    feature_of_interest = FeatureOfInterestFactory2DB(name=test_input[0])

    assert feature_of_interest.__str__() == test_output[0]
