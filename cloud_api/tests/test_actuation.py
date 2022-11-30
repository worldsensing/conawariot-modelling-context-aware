import pytest

from fixtures import ObservationFactory2DB, ThingTypeFactory2DB, ThingFactory2DB, SensorFactory2DB, \
    ActuationFactory2DB, ContextAwareRuleFactory2DB


@pytest.fixture
def create_thing_type():
    return ThingTypeFactory2DB(name="Inclinometer")


@pytest.fixture
def create_thing(create_thing_type):
    return ThingFactory2DB(name="ABC-1001", type_name="Inclinometer")


@pytest.fixture
def create_sensor(create_thing):
    return SensorFactory2DB(thing_name="ABC-1001", name="RainSensorA")


@pytest.fixture
def create_observation(create_sensor):
    return ObservationFactory2DB(sensor_name="RainSensorA", time_start="2020-03-19T12:00:00+00:00")


@pytest.fixture
def create_context_aware_rule():
    return ContextAwareRuleFactory2DB(name="Rule1", executing=True)


@pytest.mark.parametrize("test_input, test_output", [
    ([0, "Rule1", "2020-03-19T12:00:00+00:00", "2020-03-19T13:00:00+00:00"],
     ["0, 0, Rule1, 2020-03-19T12:00:00+00:00, 2020-03-19T13:00:00+00:00, []"])
])
def test_actuation_ok_to_string(api_client, orm_client, create_observation,
                                create_context_aware_rule,
                                test_input, test_output):
    actuation = ActuationFactory2DB(observation_id=test_input[0],
                                    context_aware_rule_name=test_input[1],
                                    time_start=test_input[2],
                                    time_end=test_input[3])

    assert actuation.__str__() == test_output[0]


@pytest.mark.parametrize("test_input, test_output", [
    ([0, "Rule1", "2020-03-19T12:00:00+00:00", None],
     ["0, 0, Rule1, 2020-03-19T12:00:00+00:00, None, []"])
])
def test_actuation_ok_no_time_end_to_string(api_client, orm_client, create_observation,
                                            create_context_aware_rule,
                                            test_input, test_output):
    actuation = ActuationFactory2DB(observation_id=test_input[0],
                                    context_aware_rule_name=test_input[1],
                                    time_start=test_input[2])

    assert actuation.__str__() == test_output[0]
