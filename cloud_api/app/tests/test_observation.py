from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, DateTime

from app.routes import observation
from app.schemas.observable_property import ObservableProperty
from app.schemas.observation import Observation
from app.schemas.sensor import Sensor

prefix = observation.router.prefix


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


def create_observation(session: Session, time_start: DateTime = datetime.utcnow(),
                       value_int: int = 0, sensor_name: str = "Sensor1",
                       observable_property_name: str = "ObservableProperty1"):
    observation_1 = Observation(time_start=time_start, value_int=value_int, sensor_name=sensor_name,
                                observable_property_name=observable_property_name)
    session.add(observation_1)
    session.commit()


@pytest.mark.parametrize("time_start, value_int, observable_property_name, sensor_name",
                         [["2023-04-07T09:17:17.095365", 8, "ObservableProperty1", "Sensor1"],
                          ["2023-04-07T09:17:18.095365", 4, "ObservableProperty1", "Sensor1"],
                          ["2023-04-07T09:17:19.095365", 3, "ObservableProperty1", "Sensor1"]])
def test_get_observation_exist(client: TestClient, session: Session,
                               time_start: DateTime, value_int: int,
                               observable_property_name: str, sensor_name: str):
    # PRE
    create_observable_property(session)
    create_sensor(session)
    create_observation(session, time_start=time_start, value_int=value_int,
                       observable_property_name=observable_property_name, sensor_name=sensor_name)
    # TEST
    response = client.get(f"{prefix}/{1}/")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["time_start"] == time_start
    assert response.json()["value_int"] == value_int
    assert response.json()["observable_property_name"] == observable_property_name
    assert response.json()["sensor_name"] == sensor_name


@pytest.mark.parametrize("obs_id",
                         [0])
def test_get_observation_not_exist(client: TestClient,
                                   obs_id: int):
    response = client.get(f"{prefix}/{obs_id}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Observation not found"}


@pytest.mark.parametrize("time_start, value_int, observable_property_name, sensor_name",
                         [["2023-04-07T09:17:17.095365", 8, "ObservableProperty1", "Sensor1"],
                          ["2023-04-07T09:17:18.095365", 4, "ObservableProperty1", "Sensor1"],
                          ["2023-04-07T09:17:19.095365", 3, "ObservableProperty1", "Sensor1"]])
def test_create_observation(client: TestClient, session: Session,
                            time_start: DateTime, value_int: int,
                            observable_property_name: str, sensor_name: str):
    # PRE
    create_observable_property(session, name=observable_property_name)
    create_sensor(session, name=sensor_name, observable_property_name=observable_property_name)
    # TEST
    observation_json = {
        "time_start": time_start,
        "value_int": value_int,
        "observable_property_name": observable_property_name,
        "sensor_name": sensor_name,
    }
    response = client.post(f"{prefix}/", json=observation_json)
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["time_start"] == time_start
    assert response.json()["value_int"] == value_int
    assert response.json()["observable_property_name"] == observable_property_name
    assert response.json()["sensor_name"] == sensor_name


@pytest.mark.parametrize("time_start, value_int, observable_property_name, sensor_name",
                         [["2023-04-07T09:17:17.095365", 8, "ObservableProperty1", "Sensor1"],
                          ["2023-04-07T09:17:18.095365", 4, "ObservableProperty1", "Sensor1"],
                          ["2023-04-07T09:17:19.095365", 3, "ObservableProperty1", "Sensor1"]])
def test_delete_observation_exist(client: TestClient, session: Session,
                                  time_start: DateTime, value_int: int,
                                  observable_property_name: str, sensor_name: str):
    # PRE
    create_observable_property(session)
    create_sensor(session)
    create_observation(session, time_start=time_start, value_int=value_int,
                       observable_property_name=observable_property_name, sensor_name=sensor_name)
    # TEST
    response = client.delete(f"{prefix}/{1}/")
    assert response.status_code == 200
    assert response.json()["id"] == 1


@pytest.mark.parametrize("obs_id",
                         [1])
def test_delete_observation_not_exist(client: TestClient, session: Session,
                                      obs_id: int):
    response = client.delete(f"{prefix}/{1}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Observation not found"}
