import json

import pytest

from fixtures import ThingFactory2DB, ThingTypeFactory2DB, SensorFactory2DB, ActuationDictFactory, \
    ActuationFactory2DB, ObservationFactory2DB, \
    ContextAwareRuleFactory2DB
from models import Actuation
from translators import model_translators


def assert_actuations(actuation_api, actuation_db):
    # assert actuation_db["id"] == actuation_api["id"]
    assert actuation_db["observation_id"] == actuation_api["observation_id"]
    assert actuation_db["context_aware_rule_name"] == \
           str(actuation_api["context_aware_rule_name"])
    if isinstance(actuation_db["time_start"], str):
        assert actuation_db["time_start"] == actuation_api["time_start"]
    else:
        assert model_translators.translate_datetime(actuation_db["time_start"]) == \
               actuation_api["time_start"]
    # TODO Check time_end


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
def create_context_aware_rule_2():
    return ContextAwareRuleFactory2DB(name="Rule2", executing=True)


@pytest.fixture
def create_context_aware_rule():
    return ContextAwareRuleFactory2DB(name="Rule1", executing=True)


@pytest.mark.parametrize("test_input, test_input_2", [
    ([0, "Rule1", "2020-03-19T12:00:00+00:00", "2020-03-19T13:00:00+00:00"],
     [0, "Rule2", "2020-03-19T12:00:01+00:00", "2020-03-19T13:00:00+00:00"])
])
def test_get_actuations_all(api_client, orm_client, create_observation,
                            create_context_aware_rule, create_context_aware_rule_2,
                            test_input, test_input_2):
    assert orm_client.session.query(Actuation).count() == 0
    actuation_1 = ActuationFactory2DB(observation_id=test_input[0],
                                      context_aware_rule_name=test_input[1],
                                      time_start=test_input[2],
                                      time_end=test_input[3])
    assert orm_client.session.query(Actuation).count() == 1
    actuation_2 = ActuationFactory2DB(observation_id=test_input_2[0],
                                      context_aware_rule_name=test_input_2[1],
                                      time_start=test_input_2[2],
                                      time_end=test_input_2[3])
    assert orm_client.session.query(Actuation).count() == 2

    rv = api_client.get(f"/actuations/")
    assert rv.status_code == 200
    response_content_1 = json.loads(rv.data)['data'][0]
    response_content_2 = json.loads(rv.data)['data'][1]
    assert_actuations(response_content_1, actuation_1.__dict__)
    assert_actuations(response_content_2, actuation_2.__dict__)


@pytest.mark.parametrize("test_input", [
    ([0, "Rule1", "2020-03-19T12:00:00+00:00", "2020-03-19T13:00:00+00:00"])
])
def test_get_actuation(api_client, orm_client, create_observation, create_context_aware_rule,
                       test_input):
    assert orm_client.session.query(Actuation).count() == 0
    actuation_1 = ActuationFactory2DB(observation_id=test_input[0],
                                      context_aware_rule_name=test_input[1],
                                      time_start=test_input[2],
                                      time_end=test_input[3])
    assert orm_client.session.query(Actuation).count() == 1

    rv = api_client.get(f"/actuations/{actuation_1.id}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_actuations(response_content, actuation_1.__dict__)


@pytest.mark.parametrize("test_input", [
    ([0, "Rule1", "2020-03-19T12:00:00+00:00", "2020-03-19T13:00:00+00:00"])
])
def test_add_actuation(api_client, orm_client, create_observation, create_context_aware_rule,
                       test_input):
    assert orm_client.session.query(Actuation).count() == 0
    actuation_1 = ActuationDictFactory(observation_id=test_input[0],
                                       context_aware_rule_name=test_input[1],
                                       time_start=test_input[2],
                                       time_end=test_input[3])
    assert orm_client.session.query(Actuation).count() == 0

    rv = api_client.post("/actuations/", json=actuation_1)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)['data']['id']

    # TODO Change to orm_client.session.query...
    rv = api_client.get(f"/actuations/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_actuations(response_content, actuation_1)


@pytest.mark.parametrize("test_input, test_modify", [
    ([0, "Rule1", "2020-03-19T12:00:00+00:00", None],
     [0, "Rule1", "2020-03-19T12:00:00+00:00", "2020-03-19T12:00:00.100+00:00"])
])
def test_update_actuation(api_client, orm_client, create_observation, create_context_aware_rule,
                          test_input, test_modify):
    assert orm_client.session.query(Actuation).count() == 0
    actuation_1 = ActuationFactory2DB(observation_id=test_input[0],
                                      context_aware_rule_name=test_input[1],
                                      time_start=test_input[2],
                                      time_end=test_input[3])
    assert orm_client.session.query(Actuation).count() == 1

    actuation_to_modify = ActuationDictFactory(observation_id=test_modify[0],
                                               context_aware_rule_name=test_modify[1],
                                               time_start=test_modify[2],
                                               time_end=test_modify[3])

    rv = api_client.put(f"/actuations/{actuation_1.id}",
                        json=actuation_to_modify)
    assert rv.status_code == 200
    assert orm_client.session.query(Actuation).count() == 1

    rv = api_client.get(f"/actuations/{actuation_1.id}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_actuations(response_content, actuation_to_modify)


@pytest.mark.parametrize("test_input, test_modify_1, test_modify_2, test_modify_final", [
    ([0, "Rule1", None, None],
     ["2020-03-19T12:00:00+00:00"],
     ["2020-03-19T12:00:00.100+00:00"],
     [0, "Rule1", "2020-03-19T12:00:00+00:00", "2020-03-19T12:00:00.100+00:00"])
])
def test_patch_actuation(api_client, orm_client, create_observation, create_context_aware_rule,
                         test_input, test_modify_1, test_modify_2, test_modify_final):
    assert orm_client.session.query(Actuation).count() == 0
    actuation_1 = ActuationFactory2DB(observation_id=test_input[0],
                                      context_aware_rule_name=test_input[1],
                                      time_start=test_input[2],
                                      time_end=test_input[3])
    assert orm_client.session.query(Actuation).count() == 1

    actuation_to_modify = {
        "time_start": test_modify_1[0]
    }

    rv = api_client.patch(f"/actuations/{actuation_1.id}",
                          json=actuation_to_modify)
    assert rv.status_code == 200
    assert orm_client.session.query(Actuation).count() == 1

    actuation_to_modify = {
        "time_end": test_modify_2[0]
    }

    rv = api_client.patch(f"/actuations/{actuation_1.id}",
                          json=actuation_to_modify)
    assert rv.status_code == 200
    assert orm_client.session.query(Actuation).count() == 1

    rv = api_client.get(f"/actuations/{actuation_1.id}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']

    actuation_final = ActuationDictFactory(observation_id=test_modify_final[0],
                                           context_aware_rule_name=test_modify_final[1],
                                           time_start=test_modify_final[2],
                                           time_end=test_modify_final[3])

    assert_actuations(response_content, actuation_final)


@pytest.mark.parametrize("test_input", [
    ([0, "Rule1", "2020-03-19T12:00:00+00:00", "2020-03-19T13:00:00+00:00"])
])
def test_delete_actuation(api_client, orm_client, create_observation, create_context_aware_rule,
                          test_input):
    assert orm_client.session.query(Actuation).count() == 0
    actuation_1 = ActuationFactory2DB(observation_id=test_input[0],
                                      context_aware_rule_name=test_input[1],
                                      time_start=test_input[2],
                                      time_end=test_input[3])
    assert orm_client.session.query(Actuation).count() == 1

    rv = api_client.delete(f"/actuations/{actuation_1.id}")
    assert rv.status_code == 200

    assert orm_client.session.query(Actuation).count() == 0
