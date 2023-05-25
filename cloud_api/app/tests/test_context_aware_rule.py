import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.routes import context_aware_rule
from app.schemas.context_aware_rule import ContextAwareRule

prefix = context_aware_rule.router.prefix


# TODO Add checks for EventRules, ConditionRules, and ResponseProcedures

def create_context_aware_rule(session: Session, name: str):
    context_aware_rule_1 = ContextAwareRule(name=name)
    session.add(context_aware_rule_1)
    session.commit()


@pytest.mark.parametrize("name",
                         ["ContextAwareRule1", "ContextAwareRule2"])
def test_get_context_aware_rule_exist(client: TestClient, session: Session,
                                      name: str):
    # PRE
    create_context_aware_rule(session, name)
    # TEST
    response = client.get(f"{prefix}/{name}/")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == name


@pytest.mark.parametrize("name",
                         ["NonExistingName"])
def test_get_context_aware_rule_not_exist(client: TestClient,
                                          name: str):
    response = client.get(f"{prefix}/{name}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "ContextAwareRule not found"}


@pytest.mark.parametrize("name, executing",
                         [["ContextAwareRule1", True],
                          ["ContextAwareRule2", False]])
def test_create_context_aware_rule(client: TestClient,
                                   name, executing):
    context_aware_rule_json = {
        "name": name,
        "executing": executing
    }
    response = client.post(f"{prefix}/", json=context_aware_rule_json)
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == name
    assert response.json()["executing"] == executing


@pytest.mark.parametrize("name",
                         ["ContextAwareRule1",
                          "ContextAwareRule2"])
def test_delete_context_aware_rule_exist(client: TestClient, session: Session,
                                         name: str):
    # PRE
    create_context_aware_rule(session, name)
    # TEST
    response = client.delete(f"{prefix}/{name}/")
    assert response.status_code == 200
    assert response.json()["id"] == 1


@pytest.mark.parametrize("name",
                         ["ContextAwareRule1"])
def test_delete_context_aware_rule_not_exist(client: TestClient, session: Session,
                                             name: str):
    response = client.delete(f"{prefix}/{name}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "ContextAwareRule not found"}
