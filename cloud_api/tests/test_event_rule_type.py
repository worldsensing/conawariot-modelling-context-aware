import pytest

from fixtures import EventRuleTypeFactory2DB


@pytest.mark.parametrize("test_input, test_output", [
    (["ERT1", "SENSOR_CONSTANT", "EQUALS", "INTEGER"],
     ["0, ERT1, SENSOR_CONSTANT, EQUALS, INTEGER, []"])
])
def test_event_rule_type_to_string(api_client, orm_client,
                                   test_input, test_output):
    event_rule = EventRuleTypeFactory2DB(
        name=test_input[0],
        event_rule_type=test_input[1],
        event_rule_comparation_type=test_input[2],
        event_rule_value_type=test_input[3])

    assert event_rule.__str__() == test_output[0]
