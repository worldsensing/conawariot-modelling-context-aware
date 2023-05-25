from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.repository import event_rule as event_rule_repo, sensor as sensor_repo, \
    context_aware_rule as context_aware_rule_repo, event_rule_type as event_rule_type_repo
from app.schemas.event_rule import EventRule

router = APIRouter(prefix="/event-rules")


@router.get("/", response_model=List[EventRule])
def get_event_rules(offset: int = 0, limit: int = Query(default=100, lte=100),
                    session: Session = Depends(get_session)):
    event_rules = event_rule_repo.get_event_rules(offset=offset, limit=limit, session=session)
    return event_rules


@router.post("/", response_model=EventRule)
def post_event_rule(event_rule: EventRule,
                    session: Session = Depends(get_session)):
    db_event_rule = event_rule_repo.get_event_rule(
        event_rule_name=event_rule.name, session=session)
    if db_event_rule:
        raise HTTPException(status_code=400, detail="EventRule name already registered")

    db_context_aware_rule = context_aware_rule_repo.get_context_aware_rule(
        context_aware_rule_name=event_rule.context_aware_rule_name, session=session)
    if not db_context_aware_rule:
        raise HTTPException(status_code=404, detail="ContextAwareRule does not exist")

    db_event_rule_type = event_rule_type_repo.get_event_rule_type(
        event_rule_type_name=event_rule.event_rule_type_name, session=session)
    if not db_event_rule_type:
        raise HTTPException(status_code=404, detail="EventRuleType does not exist")

    db_sensor_1 = sensor_repo.get_sensor(sensor_name=event_rule.sensor_1_name, session=session)
    if not db_sensor_1:
        raise HTTPException(status_code=404, detail="Sensor1 does not exist")

    if event_rule.sensor_2_name:
        db_sensor_2 = sensor_repo.get_sensor(sensor_name=event_rule.sensor_2_name, session=session)
        if not db_sensor_2:
            raise HTTPException(status_code=404, detail="Sensor2 does not exist")

    return event_rule_repo.create_event_rule(
        event_rule=event_rule, session=session)


@router.get("/{event_rule_name}/", response_model=EventRule)
def get_event_rule(event_rule_name: str,
                   session: Session = Depends(get_session)):
    db_event_rule = event_rule_repo.get_event_rule(
        event_rule_name=event_rule_name, session=session)
    if db_event_rule is None:
        raise HTTPException(status_code=404, detail="EventRule not found")

    return db_event_rule


@router.delete("/{event_rule_name}/", response_model=EventRule)
def delete_event_rule(event_rule_name: str,
                      session: Session = Depends(get_session)):
    get_event_rule(event_rule_name=event_rule_name, session=session)

    db_event_rule = event_rule_repo.delete_event_rule(
        event_rule_name=event_rule_name, session=session)
    return db_event_rule
