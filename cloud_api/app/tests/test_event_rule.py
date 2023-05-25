import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.routes import event_rule
from app.schemas.context_aware_rule import ContextAwareRule
from app.schemas.event_rule import EventRule
from app.schemas.event_rule_type import EventRuleType
from app.schemas.sensor import Sensor

prefix = event_rule.router.prefix


def create_context_aware_rule(session: Session, name: str = "ContextAwareRuleX"):
    context_aware_rule_1 = ContextAwareRule(name=name)
    session.add(context_aware_rule_1)
    session.commit()


def create_event_rule_type(session: Session, name: str = "EventRuleTypeX",
                           event_rule_type: str = "SENSOR_SENSOR",
                           event_rule_comparation_type: str = "EQUALS",
                           event_rule_value_type: str = "INTEGER"):
    event_rule_type_1 = EventRuleType(name=name, event_rule_type=event_rule_type,
                                      event_rule_comparation_type=event_rule_comparation_type,
                                      event_rule_value_type=event_rule_value_type)
    session.add(event_rule_type_1)
    session.commit()


def create_sensor(session: Session, name: str = "SensorX", thing_name: str = "Thing1",
                  location_name: str = "Location1",
                  observable_property_name: str = "ObservableProperty1"):
    sensor_1 = Sensor(name=name,
                      thing_name=thing_name,
                      location_name=location_name,
                      observable_property_name=observable_property_name)
    session.add(sensor_1)
    session.commit()


def create_event_rule(session: Session, name: str = "EventRule1",
                      context_aware_rule_name: str = "ContextAwareRule1",
                      event_rule_type_name: str = "EventRuleType1",
                      sensor_1_name: str = "Sensor1",
                      value_to_compare_integer: int = 0):
    event_rule_1 = EventRule(name=name, context_aware_rule_name=context_aware_rule_name,
                             event_rule_type_name=event_rule_type_name,
                             sensor_1_name=sensor_1_name,
                             value_to_compare_integer=value_to_compare_integer)
    session.add(event_rule_1)
    session.commit()


@pytest.mark.parametrize("name",
                         ["EventRule1",
                          "EventRule2"])
def test_get_event_rule_exist(client: TestClient, session: Session,
                              name: str):
    # PRE
    create_event_rule(session, name)
    # TEST
    response = client.get(f"{prefix}/{name}/")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == name


@pytest.mark.parametrize("name",
                         ["NonExistingName"])
def test_get_event_rule_not_exist(client: TestClient,
                                  name: str):
    response = client.get(f"{prefix}/{name}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "EventRule not found"}


@pytest.mark.parametrize("name, context_aware_rule_name, event_rule_type_name, "
                         "sensor_1_name, value_to_compare_integer",
                         [["EventRule1", "ContextAwareRule1", "EventRuleType1", "Sensor1", 0],
                          ["EventRule2", "ContextAwareRule1", "EventRuleType1", "Sensor1", 10]])
def test_create_event_rule(client: TestClient, session: Session,
                           name, context_aware_rule_name, event_rule_type_name, sensor_1_name,
                           value_to_compare_integer):
    # PRE
    create_context_aware_rule(session=session, name=context_aware_rule_name)
    create_event_rule_type(session=session, name=event_rule_type_name)
    create_sensor(session=session, name=sensor_1_name)
    # TEST
    event_rule_json = {
        "name": name,
        "context_aware_rule_name": context_aware_rule_name,
        "event_rule_type_name": event_rule_type_name,
        "sensor_1_name": sensor_1_name,
        "value_to_compare_integer": value_to_compare_integer,
    }
    response = client.post(f"{prefix}/", json=event_rule_json)
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == name


@pytest.mark.parametrize("name",
                         ["EventRule1",
                          "EventRule2"])
def test_delete_event_rule_exist(client: TestClient, session: Session,
                                 name: str):
    # PRE
    create_event_rule(session, name)
    # TEST
    response = client.delete(f"{prefix}/{name}/")
    assert response.status_code == 200
    assert response.json()["id"] == 1


@pytest.mark.parametrize("name",
                         ["EventRule1"])
def test_delete_event_rule_not_exist(client: TestClient, session: Session,
                                     name: str):
    response = client.delete(f"{prefix}/{name}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "EventRule not found"}
