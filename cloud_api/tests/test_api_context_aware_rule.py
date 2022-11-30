import json

import pytest

from fixtures import ContextAwareRuleFactory2DB, ContextAwareRuleDictFactory
from models import ContextAwareRule


def assert_context_aware_rules(context_aware_rule_api, context_aware_rule_db):
    # assert context_aware_rule_db["id"] == context_aware_rule_api["id"]
    assert context_aware_rule_db["name"] == context_aware_rule_api["name"]
    assert context_aware_rule_db["executing"] == context_aware_rule_api["executing"]


@pytest.mark.parametrize("test_input, test_input_2", [
    (["Rule1", True],
     ["Rule2", True])
])
def test_get_context_aware_rules_all(api_client, orm_client,
                                     test_input, test_input_2):
    assert orm_client.session.query(ContextAwareRule).count() == 0
    context_aware_rule_1 = ContextAwareRuleFactory2DB(
        name=test_input[0],
        executing=test_input[1])
    assert orm_client.session.query(ContextAwareRule).count() == 1
    context_aware_rule_2 = ContextAwareRuleFactory2DB(
        name=test_input_2[0],
        executing=test_input_2[1])
    assert orm_client.session.query(ContextAwareRule).count() == 2

    rv = api_client.get(f"/context-aware-rules/")
    assert rv.status_code == 200
    response_content_1 = json.loads(rv.data)['data'][0]
    response_content_2 = json.loads(rv.data)['data'][1]
    assert_context_aware_rules(response_content_1, context_aware_rule_1.__dict__)
    assert_context_aware_rules(response_content_2, context_aware_rule_2.__dict__)


@pytest.mark.parametrize("test_input", [
    (["Rule1", True])
])
def test_get_context_aware_rule(api_client, orm_client,
                                test_input):
    assert orm_client.session.query(ContextAwareRule).count() == 0
    context_aware_rule_1 = ContextAwareRuleFactory2DB(
        name=test_input[0],
        executing=test_input[1], )
    assert orm_client.session.query(ContextAwareRule).count() == 1

    rv = api_client.get(f"/context-aware-rules/{context_aware_rule_1.name}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_context_aware_rules(response_content, context_aware_rule_1.__dict__)


@pytest.mark.parametrize("test_input", [
    (["Rule1", True])
])
def test_add_context_aware_rule(api_client, orm_client,
                                test_input):
    assert orm_client.session.query(ContextAwareRule).count() == 0
    context_aware_rule_1 = ContextAwareRuleDictFactory(
        name=test_input[0],
        executing=test_input[1])
    assert orm_client.session.query(ContextAwareRule).count() == 0

    rv = api_client.post("/context-aware-rules/", json=context_aware_rule_1)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)['data']['name']

    # TODO Change to orm_client.session.query...
    rv = api_client.get(f"/context-aware-rules/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_context_aware_rules(response_content, context_aware_rule_1)


@pytest.mark.parametrize("test_input, test_modify", [
    (["Rule1", True],
     ["Rule1", True],)
])
def test_update_context_aware_rule(api_client, orm_client,
                                   test_input, test_modify):
    assert orm_client.session.query(ContextAwareRule).count() == 0
    context_aware_rule_1 = ContextAwareRuleFactory2DB(
        name=test_input[0],
        executing=test_input[1])
    assert orm_client.session.query(ContextAwareRule).count() == 1

    context_aware_rule_to_modify = ContextAwareRuleDictFactory(
        name=test_modify[0],
        executing=test_modify[1])

    rv = api_client.put(f"/context-aware-rules/{context_aware_rule_1.name}",
                        json=context_aware_rule_to_modify)
    assert rv.status_code == 200
    assert orm_client.session.query(ContextAwareRule).count() == 1

    rv = api_client.get(f"/context-aware-rules/{context_aware_rule_1.name}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_context_aware_rules(response_content, context_aware_rule_to_modify)


@pytest.mark.parametrize("test_input", [
    (["Rule1", True])
])
def test_delete_context_aware_rule(api_client, orm_client,
                                   test_input):
    assert orm_client.session.query(ContextAwareRule).count() == 0
    context_aware_rule_1 = ContextAwareRuleFactory2DB(
        name=test_input[0],
        executing=test_input[1])
    assert orm_client.session.query(ContextAwareRule).count() == 1

    rv = api_client.delete(f"/context-aware-rules/{context_aware_rule_1.name}")
    assert rv.status_code == 200

    assert orm_client.session.query(ContextAwareRule).count() == 0
