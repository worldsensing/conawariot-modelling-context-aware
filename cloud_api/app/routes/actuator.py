from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.repository import actuator as actuator_repo, thing as thing_repo, \
    actuatable_property as actuatable_property_repo, response_procedure as response_procedure_repo, \
    location as location_repo
from app.schemas.actuator import Actuator

router = APIRouter(prefix="/actuators")


@router.get("/", response_model=List[Actuator])
def get_actuators(offset: int = 0, limit: int = Query(default=100, lte=100),
                  session: Session = Depends(get_session)):
    actuators = actuator_repo.get_actuators(offset=offset, limit=limit, session=session)
    return actuators


@router.post("/", response_model=Actuator)
def post_actuator(actuator: Actuator,
                  session: Session = Depends(get_session)):
    db_actuator = actuator_repo.get_actuator(actuator_name=actuator.name, session=session)
    if db_actuator:
        raise HTTPException(status_code=400, detail="Actuator name already registered")

    db_thing = thing_repo.get_thing(thing_name=actuator.thing_name, session=session)
    if not db_thing:
        raise HTTPException(status_code=404, detail="Thing does not exist")

    db_actuatable_property = actuatable_property_repo.get_actuatable_property(
        actuatable_property_name=actuator.actuatable_property_name, session=session)
    if not db_actuatable_property:
        raise HTTPException(status_code=404, detail="ActuatableProperty does not exist")

    if actuator.response_procedure_name:
        db_response_procedure = response_procedure_repo.get_response_procedure(
            response_procedure_name=actuator.response_procedure_name, session=session)
        if not db_response_procedure:
            raise HTTPException(status_code=404, detail="ResponseProcedure does not exist")

    if actuator.location_name:
        db_location = location_repo.get_location(location_name=actuator.location_name,
                                                 session=session)
        if not db_location:
            raise HTTPException(status_code=404, detail="Location does not exist")

    return actuator_repo.create_actuator(
        actuator=actuator, session=session)


@router.get("/{actuator_name}/", response_model=Actuator)
def get_actuator(actuator_name: str,
                 session: Session = Depends(get_session)):
    db_actuator = actuator_repo.get_actuator(actuator_name=actuator_name, session=session)
    if db_actuator is None:
        raise HTTPException(status_code=404, detail="Actuator not found")

    return db_actuator


@router.delete("/{actuator_name}/", response_model=Actuator)
def delete_actuator(actuator_name: str,
                    session: Session = Depends(get_session)):
    get_actuator(actuator_name=actuator_name, session=session)

    db_actuator = actuator_repo.delete_actuator(actuator_name=actuator_name, session=session)
    return db_actuator
