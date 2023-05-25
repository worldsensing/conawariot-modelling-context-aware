import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.routes import actuator
from app.schemas.actuatable_property import ActuatableProperty
from app.schemas.actuator import Actuator
from app.schemas.thing import Thing

prefix = actuator.router.prefix


def create_thing(session: Session, name: str = "Thing1"):
    thing_1 = Thing(name=name)
    session.add(thing_1)
    session.commit()


def create_actuatable_property(session: Session,
                               name: str = "ActuatableProperty1",
                               feature_of_interest_name: str = "FeatureOfInterest1",
                               type_of_actuator: str = "integer"):
    actuatable_property_1 = ActuatableProperty(name=name,
                                               feature_of_interest_name=feature_of_interest_name,
                                               type_of_actuator=type_of_actuator)
    session.add(actuatable_property_1)
    session.commit()


def create_actuator(session: Session, name: str = "Actuator1", thing_name: str = "Thing1",
                    actuatable_property_name: str = "ActuatableProperty1"):
    actuator_1 = Actuator(name=name, thing_name=thing_name,
                          actuatable_property_name=actuatable_property_name)
    session.add(actuator_1)
    session.commit()


@pytest.mark.parametrize("name, thing_name, actuatable_property_name",
                         [["Actuator1", "Thing1", "ActuatableProperty1"],
                          ["Actuator2", "Thing2", "ActuatableProperty1"],
                          ["Actuator3", "Thing1", "ActuatableProperty2"]])
def test_get_actuator_exist(client: TestClient, session: Session,
                            name: str, thing_name: str, actuatable_property_name: str):
    # PRE
    create_actuator(session, name=name, thing_name=thing_name,
                    actuatable_property_name=actuatable_property_name)
    create_actuatable_property(session)
    # TEST
    response = client.get(f"{prefix}/{name}/")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == name
    assert response.json()["thing_name"] == thing_name
    assert response.json()["actuatable_property_name"] == actuatable_property_name


@pytest.mark.parametrize("name",
                         ["Actuator1"])
def test_get_actuator_not_exist(client: TestClient,
                                name: str):
    response = client.get(f"{prefix}/{name}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Actuator not found"}


@pytest.mark.parametrize("name, thing_name, actuatable_property_name",
                         [["Actuator1", "Thing1", "ActuatableProperty1"],
                          ["Actuator2", "Thing2", "ActuatableProperty1"],
                          ["Actuator3", "Thing1", "ActuatableProperty2"]])
def test_create_actuator(client: TestClient, session: Session,
                         name: str, thing_name: str, actuatable_property_name: str):
    # PRE
    create_actuatable_property(session, name=actuatable_property_name)
    create_thing(session, name=thing_name)
    # TEST
    actuator_json = {
        "name": name,
        "thing_name": thing_name,
        "actuatable_property_name": actuatable_property_name,
    }
    response = client.post(f"{prefix}/", json=actuator_json)
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == name
    assert response.json()["thing_name"] == thing_name
    assert response.json()["actuatable_property_name"] == actuatable_property_name


@pytest.mark.parametrize("name, thing_name, actuatable_property_name",
                         [["Actuator1", "Thing1", "ActuatableProperty1"],
                          ["Actuator2", "Thing2", "ActuatableProperty1"],
                          ["Actuator3", "Thing1", "ActuatableProperty2"]])
def test_delete_actuator_exist(client: TestClient, session: Session,
                               name: str, thing_name: str, actuatable_property_name: str):
    # PRE
    create_actuator(session, name=name, thing_name=thing_name,
                    actuatable_property_name=actuatable_property_name)
    create_actuatable_property(session)
    # TEST
    response = client.delete(f"{prefix}/{name}/")
    assert response.status_code == 200
    assert response.json()["id"] == 1


@pytest.mark.parametrize("name",
                         ["Actuator1"])
def test_delete_actuator_not_exist(client: TestClient, session: Session,
                                   name: str):
    response = client.delete(f"{prefix}/{name}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Actuator not found"}
