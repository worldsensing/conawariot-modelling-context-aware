import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.routes import location
from app.schemas.location import Location

prefix = location.router.prefix


def create_location(session: Session, name: str):
    location_1 = Location(name=name)
    session.add(location_1)
    session.commit()


@pytest.mark.parametrize("name",
                         ["Barcelona",
                          "Vienna"])
def test_get_location_exist(client: TestClient, session: Session,
                            name: str):
    # PRE
    create_location(session, name)
    # TEST
    response = client.get(f"{prefix}/{name}/")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == name
    assert response.json()["geo_feature"] is None
    assert response.json()["geo_coordinates"] is None


@pytest.mark.parametrize("name",
                         ["NonExistingName"])
def test_get_location_not_exist(client: TestClient,
                                name: str):
    response = client.get(f"{prefix}/{name}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Location not found"}


@pytest.mark.parametrize("name, geo_feature, geo_coordinates",
                         [["Location1", "Barcelona", "41.2, 2.2"],
                          ["Location2", "Vienna", None]])
def test_create_location(client: TestClient,
                         name, geo_feature, geo_coordinates):
    location_json = {
        "name": name,
        "geo_feature": geo_feature,
        "geo_coordinates": geo_coordinates
    }
    response = client.post(f"{prefix}/", json=location_json)
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == name
    assert response.json()["geo_feature"] == geo_feature
    assert response.json()["geo_coordinates"] == geo_coordinates


@pytest.mark.parametrize("name",
                         ["Location1",
                          "Location2"])
def test_delete_location_exist(client: TestClient, session: Session,
                               name: str):
    # PRE
    create_location(session, name)
    # TEST
    response = client.delete(f"{prefix}/{name}/")
    assert response.status_code == 200
    assert response.json()["id"] == 1


@pytest.mark.parametrize("name",
                         ["Location1"])
def test_delete_location_not_exist(client: TestClient, session: Session,
                                   name: str):
    response = client.delete(f"{prefix}/{name}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Location not found"}
