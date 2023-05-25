from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.repository import condition_rule as condition_rule_repo, \
    context_aware_rule as context_aware_rule_repo, event_rule as event_rule_repo
from app.schemas.condition_rule import ConditionRule

router = APIRouter(prefix="/condition-rules")


@router.get("/", response_model=List[ConditionRule])
def get_condition_rules(offset: int = 0, limit: int = Query(default=100, lte=100),
                        session: Session = Depends(get_session)):
    condition_rules = condition_rule_repo.get_condition_rules(offset=offset, limit=limit,
                                                              session=session)
    return condition_rules


@router.post("/", response_model=ConditionRule)
def post_condition_rule(condition_rule: ConditionRule,
                        session: Session = Depends(get_session)):
    db_condition_rule = condition_rule_repo.get_condition_rule(
        condition_rule_name=condition_rule.name, session=session)
    if db_condition_rule:
        raise HTTPException(status_code=400, detail="ConditionRule name already registered")

    db_context_aware_rule = context_aware_rule_repo.get_context_aware_rule(
        context_aware_rule_name=condition_rule.context_aware_rule_name, session=session)
    if not db_context_aware_rule:
        raise HTTPException(status_code=404, detail="ContextAwareRule does not exist")

    if condition_rule.event_rule_1_name:
        db_event_rule_1 = event_rule_repo.get_event_rule(
            event_rule_name=condition_rule.event_rule_1_name,
            session=session)
        if not db_event_rule_1:
            raise HTTPException(status_code=404, detail="EventRule1 does not exist")

    if condition_rule.event_rule_2_name:
        db_event_rule_2 = event_rule_repo.get_event_rule(
            event_rule_name=condition_rule.event_rule_2_name,
            session=session)
        if not db_event_rule_2:
            raise HTTPException(status_code=404, detail="EventRule2 does not exist")

    if condition_rule.condition_rule_1_name:
        db_condition_rule_1 = condition_rule_repo.get_condition_rule(
            condition_rule_name=condition_rule.condition_rule_1_name,
            session=session)
        if not db_condition_rule_1:
            raise HTTPException(status_code=404, detail="ConditionRule1 does not exist")

    if condition_rule.condition_rule_2_name:
        db_condition_rule_2 = condition_rule_repo.get_condition_rule(
            condition_rule_name=condition_rule.condition_rule_2_name,
            session=session)
        if not db_condition_rule_2:
            raise HTTPException(status_code=404, detail="ConditionRule2 does not exist")

    return condition_rule_repo.create_condition_rule(
        condition_rule=condition_rule, session=session)


@router.get("/{condition_rule_name}/", response_model=ConditionRule)
def get_condition_rule(condition_rule_name: str,
                       session: Session = Depends(get_session)):
    db_condition_rule = condition_rule_repo.get_condition_rule(
        condition_rule_name=condition_rule_name, session=session)
    if db_condition_rule is None:
        raise HTTPException(status_code=404, detail="ConditionRule not found")

    return db_condition_rule


@router.delete("/{condition_rule_name}/", response_model=ConditionRule)
def delete_condition_rule(condition_rule_name: str,
                          session: Session = Depends(get_session)):
    db_condition_rule = condition_rule_repo.get_condition_rule(
        condition_rule_name=condition_rule_name, session=session)
    if not db_condition_rule:
        raise HTTPException(status_code=400, detail="ConditionRule name does not exist.")

    db_condition_rule = condition_rule_repo.delete_condition_rule(
        condition_rule_name=condition_rule_name, session=session)
    return db_condition_rule
