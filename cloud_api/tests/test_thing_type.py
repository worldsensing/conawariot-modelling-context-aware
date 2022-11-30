import pytest

from fixtures import ThingTypeFactory2DB


@pytest.mark.parametrize("test_input, test_output", [
    (["Inclinometer"],
     ["0, Inclinometer, []"])
])
def test_thing_type_to_string(api_client, orm_client,
                              test_input, test_output):
    thing_type = ThingTypeFactory2DB(name=test_input[0])

    assert thing_type.__str__() == test_output[0]
