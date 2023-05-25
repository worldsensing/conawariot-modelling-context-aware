from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, DateTime

from app.routes import actuation
from app.schemas.actuatable_property import ActuatableProperty
from app.schemas.actuation import Actuation
from app.schemas.actuator import Actuator

prefix = actuation.router.prefix


def create_actuator(session: Session, name: str = "Actuator1", thing_name: str = "Thing1",
                    location_name: str = "Location1",
                    actuatable_property_name: str = "ActuatableProperty1"):
    actuator_1 = Actuator(name=name,
                          thing_name=thing_name,
                          location_name=location_name,
                          actuatable_property_name=actuatable_property_name)
    session.add(actuator_1)
    session.commit()


def create_actuatable_property(session: Session,
                               name: str = "ActuatableProperty1",
                               feature_of_interest_name: str = "FeatureOfInterest1",
                               type_of_actuation: str = "integer"):
    actuatable_property_1 = ActuatableProperty(name=name,
                                               feature_of_interest_name=feature_of_interest_name,
                                               type_of_actuation=type_of_actuation)
    session.add(actuatable_property_1)
    session.commit()


def create_actuation(session: Session, time_start: DateTime = datetime.utcnow(),
                     value_int: int = 0, actuator_name: str = "Actuator1",
                     actuatable_property_name: str = "ActuatableProperty1"):
    actuation_1 = Actuation(time_start=time_start, value_int=value_int, actuator_name=actuator_name,
                            actuatable_property_name=actuatable_property_name)
    session.add(actuation_1)
    session.commit()


@pytest.mark.parametrize("time_start, actuatable_property_name, actuator_name",
                         [["2023-04-07T09:17:17.095365", "ActuatableProperty1", "Actuator1"],
                          ["2023-04-07T09:17:18.095365", "ActuatableProperty1", "Actuator1"],
                          ["2023-04-07T09:17:19.095365", "ActuatableProperty1", "Actuator1"]])
def test_get_actuation_exist(client: TestClient, session: Session,
                             time_start: DateTime, actuatable_property_name: str,
                             actuator_name: str):
    # PRE
    create_actuatable_property(session)
    create_actuator(session)
    create_actuation(session, time_start=time_start,
                     actuatable_property_name=actuatable_property_name, actuator_name=actuator_name)
    # TEST
    response = client.get(f"{prefix}/{1}/")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["time_start"] == time_start
    assert response.json()["actuatable_property_name"] == actuatable_property_name
    assert response.json()["actuator_name"] == actuator_name


@pytest.mark.parametrize("act_id",
                         [0])
def test_get_actuation_not_exist(client: TestClient,
                                 act_id: int):
    response = client.get(f"{prefix}/{act_id}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Actuation not found"}


@pytest.mark.parametrize("time_start, actuatable_property_name, actuator_name",
                         [["2023-04-07T09:17:17.095365", "ActuatableProperty1", "Actuator1"],
                          ["2023-04-07T09:17:18.095365", "ActuatableProperty1", "Actuator1"],
                          ["2023-04-07T09:17:19.095365", "ActuatableProperty1", "Actuator1"]])
def test_create_actuation(client: TestClient, session: Session,
                          time_start: DateTime, actuatable_property_name: str, actuator_name: str):
    # PRE
    create_actuatable_property(session, name=actuatable_property_name)
    create_actuator(session, name=actuator_name, actuatable_property_name=actuatable_property_name)
    # TEST
    actuation_json = {
        "time_start": time_start,
        "actuatable_property_name": actuatable_property_name,
        "actuator_name": actuator_name,
    }
    response = client.post(f"{prefix}/", json=actuation_json)
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["time_start"] == time_start
    assert response.json()["actuatable_property_name"] == actuatable_property_name
    assert response.json()["actuator_name"] == actuator_name


@pytest.mark.parametrize("time_start, actuatable_property_name, actuator_name",
                         [["2023-04-07T09:17:17.095365", "ActuatableProperty1", "Actuator1"],
                          ["2023-04-07T09:17:18.095365", "ActuatableProperty1", "Actuator1"],
                          ["2023-04-07T09:17:19.095365", "ActuatableProperty1", "Actuator1"]])
def test_delete_actuation_exist(client: TestClient, session: Session,
                                time_start: DateTime, actuatable_property_name: str,
                                actuator_name: str):
    # PRE
    create_actuatable_property(session)
    create_actuator(session)
    create_actuation(session, time_start=time_start,
                     actuatable_property_name=actuatable_property_name, actuator_name=actuator_name)
    # TEST
    response = client.delete(f"{prefix}/{1}/")
    assert response.status_code == 200
    assert response.json()["id"] == 1


@pytest.mark.parametrize("act_id",
                         [1])
def test_delete_actuation_not_exist(client: TestClient, session: Session,
                                    act_id: int):
    response = client.delete(f"{prefix}/{act_id}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Actuation not found"}
