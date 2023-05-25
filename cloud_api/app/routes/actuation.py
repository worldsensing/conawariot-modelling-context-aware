from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.repository import actuation as actuation_repo, actuator as actuator_repo, \
    actuatable_property as actuatable_property_repo
from app.schemas.actuation import Actuation

router = APIRouter(prefix="/actuations")


@router.get("/", response_model=List[Actuation])
def get_actuations(offset: int = 0, limit: int = Query(default=100, lte=100),
                   session: Session = Depends(get_session)):
    actuations = actuation_repo.get_actuations(offset=offset, limit=limit, session=session)
    return actuations


@router.post("/", response_model=Actuation)
def post_actuation(actuation: Actuation,
                   session: Session = Depends(get_session)):
    db_actuation = actuation_repo.get_actuation(actuation_id=actuation.id, session=session)
    if db_actuation:
        raise HTTPException(status_code=400, detail="Actuation name already registered")

    db_actuator = actuator_repo.get_actuator(actuator_name=actuation.actuator_name, session=session)
    if not db_actuator:
        raise HTTPException(status_code=404, detail="FeatureOfInterest does not exist")

    db_actuatable_property = actuatable_property_repo.get_actuatable_property(
        actuatable_property_name=actuation.actuatable_property_name, session=session)
    if not db_actuatable_property:
        raise HTTPException(status_code=404, detail="ActuatableProperty does not exist")

    return actuation_repo.create_actuation(
        actuation=actuation, session=session)


@router.get("/{actuation_id}/", response_model=Actuation)
def get_actuation(actuation_id: int,
                  session: Session = Depends(get_session)):
    db_actuation = actuation_repo.get_actuation(actuation_id=actuation_id, session=session)
    if db_actuation is None:
        raise HTTPException(status_code=404, detail="Actuation not found")

    return db_actuation


@router.delete("/{actuation_id}/", response_model=Actuation)
def delete_actuation(actuation_id: int,
                     session: Session = Depends(get_session)):
    get_actuation(actuation_id=actuation_id, session=session)

    db_actuation = actuation_repo.delete_actuation(actuation_id=actuation_id, session=session)
    return db_actuation
