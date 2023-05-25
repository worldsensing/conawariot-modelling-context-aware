from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.repository import actuatable_property as actuatable_property_repo, \
    feature_of_interest as feature_of_interest_repo
from app.schemas.actuatable_property import ActuatableProperty
from app.schemas.actuation import Actuation
from app.schemas.actuator import Actuator

router = APIRouter(prefix="/actuatable-properties")


@router.get("/", response_model=List[ActuatableProperty])
def get_actuatable_properties(offset: int = 0, limit: int = Query(default=100, lte=100),
                              session: Session = Depends(get_session)):
    actuatable_properties = actuatable_property_repo.get_actuatable_properties(offset=offset,
                                                                               limit=limit,
                                                                               session=session)
    return actuatable_properties


@router.post("/", response_model=ActuatableProperty)
def post_actuatable_property(actuatable_property: ActuatableProperty,
                             session: Session = Depends(get_session)):
    db_actuatable_property = actuatable_property_repo.get_actuatable_property(
        actuatable_property_name=actuatable_property.name, session=session)
    if db_actuatable_property:
        raise HTTPException(status_code=400, detail="ActuatableProperty name already registered")

    db_feature_of_interest = feature_of_interest_repo.get_feature_of_interest(
        feature_of_interest_name=actuatable_property.feature_of_interest_name, session=session)
    if not db_feature_of_interest:
        raise HTTPException(status_code=404, detail="FeatureOfInterest does not exist")

    return actuatable_property_repo.create_actuatable_property(
        actuatable_property=actuatable_property, session=session)


@router.get("/{actuatable_property_name}/", response_model=ActuatableProperty)
def get_actuatable_property(actuatable_property_name: str,
                            session: Session = Depends(get_session)):
    db_actuatable_property = actuatable_property_repo.get_actuatable_property(
        actuatable_property_name=actuatable_property_name, session=session)
    if db_actuatable_property is None:
        raise HTTPException(status_code=404, detail="ActuatableProperty not found")

    return db_actuatable_property


@router.get("/{actuatable_property_name}/actuators", response_model=List[Actuator])
def get_actuatable_property_actuators(actuatable_property_name: str,
                                      session: Session = Depends(get_session)):
    db_actuatable_property = get_actuatable_property(actuatable_property_name, session)

    return db_actuatable_property.actuators


@router.get("/{actuatable_property_name}/actuations", response_model=List[Actuation])
def get_actuatable_property_actuations(actuatable_property_name: str,
                                       session: Session = Depends(get_session)):
    db_actuatable_property = get_actuatable_property(actuatable_property_name, session)

    return db_actuatable_property.actuations


@router.delete("/{actuatable_property_name}/", response_model=ActuatableProperty)
def delete_actuatable_property(actuatable_property_name: str,
                               session: Session = Depends(get_session)):
    get_actuatable_property(actuatable_property_name=actuatable_property_name, session=session)

    db_actuatable_property = actuatable_property_repo.delete_actuatable_property(
        actuatable_property_name=actuatable_property_name, session=session)
    return db_actuatable_property
