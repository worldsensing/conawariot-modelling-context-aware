from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, DateTime

from app.routes import observable_property
from app.schemas.feature_of_interest import FeatureOfInterest
from app.schemas.observable_property import ObservableProperty
from app.schemas.observation import Observation
from app.schemas.sensor import Sensor

prefix = observable_property.router.prefix


def create_feature_of_interest(session: Session,
                               name: str = "FeatureOfInterest1"):
    feature_of_interest_1 = FeatureOfInterest(name=name)
    session.add(feature_of_interest_1)
    session.commit()


def create_observation(session: Session, time_start: DateTime = datetime.utcnow(),
                       sensor_name: str = "Sensor1",
                       observable_property_name: str = "ObservableProperty1"):
    observation_1 = Observation(time_start=time_start, sensor_name=sensor_name,
                                observable_property_name=observable_property_name)
    session.add(observation_1)
    session.commit()


def create_sensor(session: Session, name: str = "Sensor1", thing_name: str = "Thing1",
                  location_name: str = "Location1",
                  observable_property_name: str = "ObservableProperty1"):
    sensor_1 = Sensor(name=name,
                      thing_name=thing_name,
                      location_name=location_name,
                      observable_property_name=observable_property_name)
    session.add(sensor_1)
    session.commit()


def create_observable_property(session: Session,
                               name: str = "ObservableProperty1",
                               feature_of_interest_name: str = "FeatureOfInterest1",
                               type_of_observation: str = "integer"):
    observable_property_1 = ObservableProperty(name=name,
                                               feature_of_interest_name=feature_of_interest_name,
                                               type_of_observation=type_of_observation)
    session.add(observable_property_1)
    session.commit()


@pytest.mark.parametrize("name, feature_of_interest_name, type_of_observation",
                         [["ObservableProperty1", "FeatureOfInterest1", "integer"],
                          ["ObservableProperty2", "FeatureOfInterest2", "string"],
                          ["ObservableProperty3", "FeatureOfInterest3", "dict"]])
def test_get_observable_property_exist(client: TestClient, session: Session,
                                       name: str, feature_of_interest_name: str,
                                       type_of_observation: str):
    # PRE
    create_observable_property(session, name, feature_of_interest_name, type_of_observation)
    # TEST
    response = client.get(f"{prefix}/{name}/")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == name
    assert response.json()["feature_of_interest_name"] == feature_of_interest_name


@pytest.mark.parametrize("name",
                         ["NonExistingName"])
def test_get_observable_property_not_exist(client: TestClient,
                                           name: str):
    response = client.get(f"{prefix}/{name}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "ObservableProperty not found"}


@pytest.mark.parametrize("name, feature_of_interest_name, type_of_observation",
                         [["ObservableProperty1", "FeatureOfInterest1", "integer"]])
def test_get_observable_property_sensors(client: TestClient, session: Session,
                                         name: str, feature_of_interest_name: str,
                                         type_of_observation: str):
    # PRE
    sensor_name = "Sensor1"
    create_sensor(session, name=sensor_name, observable_property_name=name)
    create_observable_property(session, name, feature_of_interest_name, type_of_observation)
    # TEST
    response = client.get(f"{prefix}/{name}/sensors")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 1
    assert response.json()[0]["name"] == sensor_name


@pytest.mark.parametrize("name, feature_of_interest_name, type_of_observation",
                         [["ObservableProperty1", "FeatureOfInterest1", "integer"],
                          ["ObservableProperty2", "FeatureOfInterest2", "string"],
                          ["ObservableProperty3", "FeatureOfInterest3", "dict"]])
def test_get_observable_property_observations(client: TestClient, session: Session,
                                              name: str, feature_of_interest_name: str,
                                              type_of_observation: str):
    # PRE
    sensor_name = "Sensor1"
    create_observation(session, sensor_name=sensor_name, observable_property_name=name)
    create_sensor(session, name=sensor_name, observable_property_name=name)
    create_observable_property(session, name, feature_of_interest_name, type_of_observation)
    # TEST
    response = client.get(f"{prefix}/{name}/observations")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 1
    assert response.json()[0]["sensor_name"] == sensor_name


@pytest.mark.parametrize("name, feature_of_interest_name, type_of_observation",
                         [["ObservableProperty1", "FeatureOfInterest1", "integer"],
                          ["ObservableProperty2", "FeatureOfInterest2", "string"],
                          ["ObservableProperty3", "FeatureOfInterest3", "dict"]])
def test_create_observable_property(client: TestClient, session: Session,
                                    name: str, feature_of_interest_name: str,
                                    type_of_observation: str):
    # PRE
    create_feature_of_interest(session, name=feature_of_interest_name)
    # TEST
    observable_property_json = {
        "name": name,
        "feature_of_interest_name": feature_of_interest_name,
        "type_of_observation": type_of_observation
    }
    response = client.post(f"{prefix}/", json=observable_property_json)
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == name
    assert response.json()["feature_of_interest_name"] == feature_of_interest_name


@pytest.mark.parametrize("name, feature_of_interest_name, type_of_observation",
                         [["ObservableProperty1", "FeatureOfInterest1", "integer"],
                          ["ObservableProperty2", "FeatureOfInterest2", "string"],
                          ["ObservableProperty3", "FeatureOfInterest3", "dict"]])
def test_delete_observable_property_exist(client: TestClient, session: Session,
                                          name: str, feature_of_interest_name: str,
                                          type_of_observation: str):
    # PRE
    create_observable_property(session, name, feature_of_interest_name, type_of_observation)
    # TEST
    response = client.delete(f"{prefix}/{name}/")
    assert response.status_code == 200
    assert response.json()["id"] == 1


@pytest.mark.parametrize("name",
                         ["ObservableProperty1"])
def test_delete_observable_property_not_exist(client: TestClient, session: Session,
                                              name: str):
    response = client.delete(f"{prefix}/{name}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "ObservableProperty not found"}
