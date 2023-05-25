from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.repository import event_rule_type as event_rule_type_repo
from app.schemas.event_rule_type import EventRuleType

router = APIRouter(prefix="/event-rule-types")


@router.get("/", response_model=List[EventRuleType])
def get_event_rule_types(offset: int = 0, limit: int = Query(default=100, lte=100),
                         session: Session = Depends(get_session)):
    event_rule_type_types = event_rule_type_repo.get_event_rule_types(offset=offset,
                                                                      limit=limit,
                                                                      session=session)
    return event_rule_type_types


@router.post("/", response_model=EventRuleType)
def post_event_rule_type(event_rule_type: EventRuleType,
                         session: Session = Depends(get_session)):
    db_event_rule_type = event_rule_type_repo.get_event_rule_type(
        event_rule_type_name=event_rule_type.name, session=session)
    if db_event_rule_type:
        raise HTTPException(status_code=400, detail="EventRuleType name already registered")

    return event_rule_type_repo.create_event_rule_type(
        event_rule_type=event_rule_type, session=session)


@router.get("/{event_rule_type_name}/", response_model=EventRuleType)
def get_event_rule_type(event_rule_type_name: str,
                        session: Session = Depends(get_session)):
    db_event_rule_type = event_rule_type_repo.get_event_rule_type(
        event_rule_type_name=event_rule_type_name, session=session)
    if db_event_rule_type is None:
        raise HTTPException(status_code=404, detail="EventRuleType not found")

    return db_event_rule_type


@router.delete("/{event_rule_type_name}/", response_model=EventRuleType)
def delete_event_rule_type(event_rule_type_name: str,
                           session: Session = Depends(get_session)):
    get_event_rule_type(event_rule_type_name=event_rule_type_name, session=session)

    db_event_rule_type = event_rule_type_repo.delete_event_rule_type(
        event_rule_type_name=event_rule_type_name, session=session)
    return db_event_rule_type
