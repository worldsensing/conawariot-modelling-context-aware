import pytest

from fixtures import PlatformFactory2DB, LocationFactory2DB


@pytest.fixture
def create_location():
    return LocationFactory2DB(name="MyLocation1")


@pytest.mark.parametrize("test_input, test_output", [
    (["PlatformA", "MyLocation1"],
     ["0, PlatformA, MyLocation1, []"])
])
def test_platform_to_string(api_client, orm_client, create_location,
                            test_input, test_output):
    platform = PlatformFactory2DB(name=test_input[0],
                                  location_name=test_input[1])

    assert platform.__str__() == test_output[0]


@pytest.mark.parametrize("test_input, test_output", [
    (["Site"],
     ["0, Site, None, []"])
])
def test_platform_no_location_to_string(api_client, orm_client,
                                        test_input, test_output):
    platform = PlatformFactory2DB(name=test_input[0])

    assert platform.__str__() == test_output[0]
