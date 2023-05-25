from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.repository import observable_property as observable_property_repo, sensor as \
    sensor_repo, observation as observation_repo
from app.schemas.observation import Observation

router = APIRouter(prefix="/observations")


@router.get("/", response_model=List[Observation])
def get_observations(offset: int = 0, limit: int = Query(default=100, lte=100),
                     session: Session = Depends(get_session)):
    db_observations = observation_repo.get_observations(offset=offset, limit=limit, session=session)
    return db_observations


@router.post("/", response_model=Observation)
def post_observations(observation: Observation,
                      session: Session = Depends(get_session)):
    db_observable_property = observable_property_repo.get_observable_property(
        observable_property_name=observation.observable_property_name, session=session)
    if not db_observable_property:
        raise HTTPException(status_code=404, detail="ObservableProperty does not exist")

    # TODO Check comparing that if the observable_property states that the data comes via
    #  Integer, there is where information should be

    db_sensor = sensor_repo.get_sensor(sensor_name=observation.sensor_name, session=session)
    if not db_sensor:
        raise HTTPException(status_code=404, detail="Sensor does not exist.")

    return observation_repo.create_observation(observation=observation, session=session)


@router.get("/{observation_id}/", response_model=Observation)
def get_observation(observation_id: int,
                    session: Session = Depends(get_session)):
    db_observation = observation_repo.get_observation_id(observation_id=observation_id,
                                                         session=session)
    if db_observation is None:
        raise HTTPException(status_code=404, detail="Observation not found")

    return db_observation


@router.get("/sensor/{sensor_name}/", response_model=List[Observation])
def get_observations(sensor_name: str,
                     session: Session = Depends(get_session)):
    db_observations = observation_repo.get_observations_sensor(sensor_name=sensor_name, offset=0,
                                                               limit=100, session=session)

    return db_observations


@router.delete("/{observation_id}/", response_model=Observation)
def delete_observation(observation_id: int,
                       session: Session = Depends(get_session)):
    get_observation(observation_id=observation_id, session=session)

    db_observation = observation_repo.delete_observation_id(observation_id=observation_id,
                                                            session=session)
    return db_observation


@router.delete("/sensor/{sensor_name}/", response_model=List[Observation])
def delete_observations(sensor_name: str, session: Session = Depends(get_session)):
    db_observations = observation_repo.delete_observations_sensor(sensor_name=sensor_name,
                                                                  session=session)
    return db_observations
