from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.repository import context_aware_rule as context_aware_rule_repo
from app.schemas.condition_rule import ConditionRule
from app.schemas.context_aware_rule import ContextAwareRule
from app.schemas.event_rule import EventRule
from app.schemas.response_procedure import ResponseProcedure

router = APIRouter(prefix="/context-aware-rules")


@router.get("/", response_model=List[ContextAwareRule])
def get_context_aware_rules(offset: int = 0, limit: int = Query(default=100, lte=100),
                            session: Session = Depends(get_session)):
    context_aware_rules = context_aware_rule_repo.get_context_aware_rules(offset=offset,
                                                                          limit=limit,
                                                                          session=session)
    return context_aware_rules


@router.post("/", response_model=ContextAwareRule)
def post_context_aware_rule(context_aware_rule: ContextAwareRule,
                            session: Session = Depends(get_session)):
    db_context_aware_rule = context_aware_rule_repo.get_context_aware_rule(
        context_aware_rule_name=context_aware_rule.name, session=session)
    if db_context_aware_rule:
        raise HTTPException(status_code=400, detail="ContextAwareRule name already registered")

    return context_aware_rule_repo.create_context_aware_rule(
        context_aware_rule=context_aware_rule, session=session)


@router.get("/{context_aware_rule_name}/", response_model=ContextAwareRule)
def get_context_aware_rule(context_aware_rule_name: str,
                           session: Session = Depends(get_session)):
    db_context_aware_rule = context_aware_rule_repo.get_context_aware_rule(
        context_aware_rule_name=context_aware_rule_name, session=session)

    if db_context_aware_rule is None:
        raise HTTPException(status_code=404, detail="ContextAwareRule not found")
    return db_context_aware_rule


@router.get("/{context_aware_rule_name}/event-rules", response_model=List[EventRule])
def get_context_aware_rule_event_rules(context_aware_rule_name: str,
                                       session: Session = Depends(get_session)):
    db_context_aware_rule = get_context_aware_rule(context_aware_rule_name=context_aware_rule_name,
                                                   session=session)

    return db_context_aware_rule.event_rules


@router.get("/{context_aware_rule_name}/condition-rules", response_model=List[ConditionRule])
def get_context_aware_rule_event_rules(context_aware_rule_name: str,
                                       session: Session = Depends(get_session)):
    db_context_aware_rule = get_context_aware_rule(context_aware_rule_name=context_aware_rule_name,
                                                   session=session)

    return db_context_aware_rule.condition_rules


@router.get("/{context_aware_rule_name}/response-procedures",
            response_model=List[ResponseProcedure])
def get_context_aware_rule_components(context_aware_rule_name: str,
                                      session: Session = Depends(get_session)):
    db_context_aware_rule = get_context_aware_rule(context_aware_rule_name=context_aware_rule_name,
                                                   session=session)

    return db_context_aware_rule.response_procedures


@router.delete("/{context_aware_rule_name}/", response_model=ContextAwareRule)
def delete_context_aware_rule(context_aware_rule_name: str,
                              session: Session = Depends(get_session)):
    get_context_aware_rule(context_aware_rule_name=context_aware_rule_name, session=session)

    db_context_aware_rule = context_aware_rule_repo.delete_context_aware_rule(
        context_aware_rule_name=context_aware_rule_name, session=session)
    return db_context_aware_rule
