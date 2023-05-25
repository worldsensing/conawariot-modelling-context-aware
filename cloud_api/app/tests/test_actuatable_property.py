from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, DateTime

from app.routes import actuatable_property
from app.schemas.actuatable_property import ActuatableProperty
from app.schemas.actuation import Actuation
from app.schemas.actuator import Actuator
from app.schemas.feature_of_interest import FeatureOfInterest

prefix = actuatable_property.router.prefix


def create_feature_of_interest(session: Session,
                               name: str = "FeatureOfInterest1"):
    feature_of_interest_1 = FeatureOfInterest(name=name)
    session.add(feature_of_interest_1)
    session.commit()


def create_actuatable_property(session: Session,
                               name: str = "ActuatableProperty1",
                               feature_of_interest_name: str = "FeatureOfInterest1"):
    actuatable_property_1 = ActuatableProperty(name=name,
                                               feature_of_interest_name=feature_of_interest_name)
    session.add(actuatable_property_1)
    session.commit()


def create_actuation(session: Session, time_start: DateTime = datetime.utcnow(),
                     actuator_name: str = "Actuator1",
                     actuatable_property_name: str = "ActuatableProperty1"):
    actuation_1 = Actuation(time_start=time_start, actuator_name=actuator_name,
                            actuatable_property_name=actuatable_property_name)
    session.add(actuation_1)
    session.commit()


def create_actuator(session: Session, name: str = "Actuator1", thing_name: str = "Thing1",
                    actuatable_property_name: str = "ActuatableProperty1"):
    actuator_1 = Actuator(name=name,
                          thing_name=thing_name,
                          actuatable_property_name=actuatable_property_name)
    session.add(actuator_1)
    session.commit()


@pytest.mark.parametrize("name, feature_of_interest_name",
                         [["ActuatableProperty1", "FeatureOfInterest1"],
                          ["ActuatableProperty2", "FeatureOfInterest2"]])
def test_get_actuatable_property_exist(client: TestClient, session: Session,
                                       name: str, feature_of_interest_name: str):
    # PRE
    create_actuatable_property(session, name, feature_of_interest_name)
    # TEST
    response = client.get(f"{prefix}/{name}/")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == name
    assert response.json()["feature_of_interest_name"] == feature_of_interest_name


@pytest.mark.parametrize("name",
                         ["NonExistingName"])
def test_get_actuatable_property_not_exist(client: TestClient,
                                           name: str):
    response = client.get(f"{prefix}/{name}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "ActuatableProperty not found"}


@pytest.mark.parametrize("name, feature_of_interest_name",
                         [["ActuatableProperty1", "FeatureOfInterest1"],
                          ["ActuatableProperty2", "FeatureOfInterest2"]])
def test_get_actuatable_property_actuators(client: TestClient, session: Session,
                                           name: str, feature_of_interest_name: str):
    # PRE
    actuator_name = "Actuator1"
    create_actuator(session, name=actuator_name, actuatable_property_name=name)
    create_actuatable_property(session, name, feature_of_interest_name)
    # TEST
    response = client.get(f"{prefix}/{name}/actuators")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 1
    assert response.json()[0]["name"] == actuator_name


@pytest.mark.parametrize("name, feature_of_interest_name",
                         [["ActuatableProperty1", "FeatureOfInterest1"],
                          ["ActuatableProperty2", "FeatureOfInterest2"]])
def test_get_actuatable_property_actuations(client: TestClient, session: Session,
                                            name: str, feature_of_interest_name: str):
    # PRE
    actuator_name = "Actuator1"
    create_actuation(session, actuator_name=actuator_name, actuatable_property_name=name)
    create_actuator(session, name=actuator_name, actuatable_property_name=name)
    create_actuatable_property(session, name, feature_of_interest_name)
    # TEST
    response = client.get(f"{prefix}/{name}/actuations")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 1
    assert response.json()[0]["actuator_name"] == actuator_name


@pytest.mark.parametrize("name, feature_of_interest_name",
                         [["ActuatableProperty1", "FeatureOfInterest1"],
                          ["ActuatableProperty2", "FeatureOfInterest2"]])
def test_create_actuatable_property(client: TestClient, session: Session,
                                    name: str, feature_of_interest_name: str):
    # PRE
    create_feature_of_interest(session, name=feature_of_interest_name)
    # TEST
    actuatable_property_json = {
        "name": name,
        "feature_of_interest_name": feature_of_interest_name,
    }
    response = client.post(f"{prefix}/", json=actuatable_property_json)
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == name
    assert response.json()["feature_of_interest_name"] == feature_of_interest_name


@pytest.mark.parametrize("name, feature_of_interest_name",
                         [["ActuatableProperty1", "FeatureOfInterest1"]])
def test_delete_actuatable_property_exist(client: TestClient, session: Session,
                                          name: str, feature_of_interest_name: str):
    # PRE
    create_actuatable_property(session, name, feature_of_interest_name)
    # TEST
    response = client.delete(f"{prefix}/{name}/")
    assert response.status_code == 200
    assert response.json()["id"] == 1


@pytest.mark.parametrize("name",
                         ["ActuatableProperty1"])
def test_delete_actuatable_property_not_exist(client: TestClient, session: Session,
                                              name: str):
    response = client.delete(f"{prefix}/{name}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "ActuatableProperty not found"}
