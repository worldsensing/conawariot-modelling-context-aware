import pytest

from fixtures import ThingFactory2DB, ThingTypeFactory2DB, LocationFactory2DB


@pytest.fixture
def create_thing_type():
    return ThingTypeFactory2DB(name="Inclinometer")


@pytest.fixture
def create_location():
    return LocationFactory2DB(name="MyLocation1")


@pytest.mark.parametrize("test_input, test_output", [
    (["a", "Inclinometer", "MyLocation1"],
     ["0, a, Inclinometer, MyLocation1, [], [], []"])
])
def test_thing_to_string(api_client, orm_client, create_thing_type, create_location,
                         test_input, test_output):
    thing = ThingFactory2DB(name=test_input[0],
                            type_name=test_input[1],
                            location_name=test_input[2])

    assert thing.__str__() == test_output[0]


@pytest.mark.parametrize("test_input, test_output", [
    (["a", "Inclinometer"],
     ["0, a, Inclinometer, None, [], [], []"])
])
def test_thing_no_location_to_string(api_client, orm_client, create_thing_type,
                                     test_input, test_output):
    thing = ThingFactory2DB(name=test_input[0],
                            type_name=test_input[1])

    assert thing.__str__() == test_output[0]
