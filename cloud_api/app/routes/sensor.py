from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.repository import location as location_repo
from app.repository import sensor as sensor_repo, observable_property as observable_property_repo, \
    observation as observation_repo, thing as thing_repo, gateway as gateway_repo
from app.schemas.sensor import Sensor

router = APIRouter(prefix="/sensors")


@router.get("/", response_model=List[Sensor])
def get_sensors(offset: int = 0, limit: int = Query(default=100, lte=100),
                session: Session = Depends(get_session)):
    sensors = sensor_repo.get_sensors(offset=offset, limit=limit, session=session)
    return sensors


@router.post("/", response_model=Sensor)
def post_sensor(sensor: Sensor,
                session: Session = Depends(get_session)):
    db_sensor = sensor_repo.get_sensor(sensor_name=sensor.name, session=session)
    if db_sensor:
        raise HTTPException(status_code=400, detail="Sensor name already registered")

    db_observable_property = observable_property_repo.get_observable_property(
        observable_property_name=sensor.observable_property_name, session=session)
    if not db_observable_property:
        raise HTTPException(status_code=404, detail="ObservableProperty does not exist")

    if sensor.thing_name:
        db_thing = thing_repo.get_thing(thing_name=sensor.thing_name,
                                        session=session)
        if not db_thing:
            raise HTTPException(status_code=404, detail="Thing does not exist")

    if sensor.gateway_name:
        db_gateway = gateway_repo.get_gateway(gateway_name=sensor.gateway_name,
                                              session=session)
        if not db_gateway:
            raise HTTPException(status_code=404, detail="Group does not exist")

    if sensor.location_name:
        db_location = location_repo.get_location(location_name=sensor.location_name,
                                                 session=session)
        if not db_location:
            raise HTTPException(status_code=404, detail="Location name does not exist")

    return sensor_repo.create_sensor(sensor=sensor, session=session)


@router.get("/{sensor_name}/", response_model=Sensor)
def get_sensor(sensor_name: str,
               session: Session = Depends(get_session)):
    db_sensor = sensor_repo.get_sensor(sensor_name=sensor_name, session=session)
    if db_sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")

    return db_sensor


@router.delete("/{sensor_name}/", response_model=Sensor)
def delete_sensor(sensor_name: str,
                  session: Session = Depends(get_session)):
    db_sensor = sensor_repo.get_sensor(sensor_name=sensor_name, session=session)
    if not db_sensor:
        raise HTTPException(status_code=400, detail="Sensor name does not exist")

    db_observations_sensor = observation_repo.get_observations_sensor(sensor_name,
                                                                      offset=0, limit=1,
                                                                      session=session)
    if db_observations_sensor:
        raise HTTPException(status_code=400, detail="An Observation is made using this Sensor, "
                                                    "remove it first")

    db_sensor = sensor_repo.delete_sensor(sensor_name=sensor_name, session=session)
    return db_sensor
