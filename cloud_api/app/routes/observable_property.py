from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.repository import observable_property as observable_property_repo, sensor as \
    sensor_repo, observation as observation_repo, feature_of_interest as feature_of_interest_repo
from app.schemas.observable_property import ObservableProperty
from app.schemas.observation import Observation
from app.schemas.sensor import Sensor

router = APIRouter(prefix="/observable-properties")


@router.get("/", response_model=List[ObservableProperty])
def get_observable_properties(offset: int = 0, limit: int = Query(default=100, lte=100),
                              session: Session = Depends(get_session)):
    observable_property = observable_property_repo.get_observable_properties(offset=offset,
                                                                             limit=limit,
                                                                             session=session)
    return observable_property


@router.post("/", response_model=ObservableProperty)
def post_observable_property(observable_property: ObservableProperty,
                             session: Session = Depends(get_session)):
    db_observable_property = observable_property_repo.get_observable_property(
        observable_property_name=observable_property.name, session=session)
    if db_observable_property:
        raise HTTPException(status_code=400, detail="ObservableProperty name already registered")

    db_feature_of_interest = feature_of_interest_repo.get_feature_of_interest(
        feature_of_interest_name=observable_property.feature_of_interest_name, session=session)
    if not db_feature_of_interest:
        raise HTTPException(status_code=404, detail="FeatureOfInterest does not exist")

    return observable_property_repo.create_observable_property(
        observable_property=observable_property, session=session)


@router.get("/{observable_property_name}/", response_model=ObservableProperty)
def get_observable_property(observable_property_name: str,
                            session: Session = Depends(get_session)):
    db_observable_property = observable_property_repo.get_observable_property(
        observable_property_name=observable_property_name, session=session)
    if not db_observable_property:
        raise HTTPException(status_code=404, detail="ObservableProperty not found")

    return db_observable_property


@router.get("/{observable_property_name}/sensors", response_model=List[Sensor])
def get_observable_property_sensors(observable_property_name: str,
                                    session: Session = Depends(get_session)):
    db_observable_property = get_observable_property(observable_property_name, session)

    return db_observable_property.sensors


@router.get("/{observable_property_name}/observations", response_model=List[Observation])
def get_observable_property_observations(observable_property_name: str,
                                         session: Session = Depends(get_session)):
    db_observable_property = get_observable_property(observable_property_name, session)

    return db_observable_property.observations


@router.delete("/{observable_property_name}/", response_model=ObservableProperty)
def delete_observable_property(observable_property_name: str,
                               session: Session = Depends(get_session)):
    get_observable_property(observable_property_name=observable_property_name, session=session)

    db_sensor = sensor_repo.get_sensors_by_observable_property(observable_property_name, 0, 100,
                                                               session=session)
    if db_sensor:
        raise HTTPException(status_code=400, detail="A Sensor is using this ObservableProperty, "
                                                    "remove it first.")

    db_observations_sensor = observation_repo.get_observations_sensor(observable_property_name, 0,
                                                                      100, session=session)
    if db_observations_sensor:
        raise HTTPException(status_code=400,
                            detail="An Observation is using this ObservableProperty, "
                                   "remove it first.")

    db_observable_property = observable_property_repo.delete_observable_property(
        observable_property_name=observable_property_name, session=session)
    return db_observable_property
