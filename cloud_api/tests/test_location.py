import pytest

from fixtures import LocationFactory2DB


@pytest.mark.parametrize("test_input, test_output", [
    (["MyLocation1", "41,2"],
     ["0, MyLocation1, 41,2"])
])
def test_location_to_string(api_client, orm_client,
                            test_input, test_output):
    location = LocationFactory2DB(name=test_input[0],
                                  latlng=test_input[1])

    assert location.__str__() == test_output[0]


@pytest.mark.parametrize("test_input, test_output", [
    (["MyLocation1"],
     ["0, MyLocation1, None"])
])
def test_location_no_latlng_to_string(api_client, orm_client,
                                      test_input, test_output):
    location = LocationFactory2DB(name=test_input[0])

    assert location.__str__() == test_output[0]
