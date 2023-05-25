from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.repository import response_procedure as response_procedure_repo, \
    context_aware_rule as context_aware_rule_repo, actuator as actuator_repo, \
    procedure_type as procedure_type_repo
from app.schemas.response_procedure import ResponseProcedure

router = APIRouter(prefix="/response-procedures")


@router.get("/", response_model=List[ResponseProcedure])
def get_response_procedures(offset: int = 0, limit: int = Query(default=100, lte=100),
                            session: Session = Depends(get_session)):
    response_procedures = response_procedure_repo.get_response_procedures(offset=offset,
                                                                          limit=limit,
                                                                          session=session)
    return response_procedures


@router.post("/", response_model=ResponseProcedure)
def post_response_procedure(response_procedure: ResponseProcedure,
                            session: Session = Depends(get_session)):
    db_response_procedure = response_procedure_repo.get_response_procedure(
        response_procedure_name=response_procedure.name, session=session)
    if db_response_procedure:
        raise HTTPException(status_code=400, detail="ResponseProcedure name already registered")

    db_context_aware_rule = context_aware_rule_repo.get_context_aware_rule(
        context_aware_rule_name=response_procedure.context_aware_rule_name, session=session)
    if not db_context_aware_rule:
        raise HTTPException(status_code=404, detail="ContextAwareRule does not exist")

    db_actuator = actuator_repo.get_actuator(actuator_name=response_procedure.actuator_name,
                                             session=session)
    if not db_actuator:
        raise HTTPException(status_code=404, detail="Actuator does not exist")

    db_procedure_type = procedure_type_repo.get_procedure_type(
        procedure_type_name=response_procedure.procedure_type_name, session=session)
    if not db_procedure_type:
        raise HTTPException(status_code=404, detail="ProcedureType does not exist")

    return response_procedure_repo.create_response_procedure(
        response_procedure=response_procedure, session=session)


@router.get("/{response_procedure_name}/", response_model=ResponseProcedure)
def get_response_procedure(response_procedure_name: str,
                           session: Session = Depends(get_session)):
    db_response_procedure = response_procedure_repo.get_response_procedure(
        response_procedure_name=response_procedure_name, session=session)
    if db_response_procedure is None:
        raise HTTPException(status_code=404, detail="ResponseProcedure not found")

    return db_response_procedure


@router.delete("/{response_procedure_name}/", response_model=ResponseProcedure)
def delete_response_procedure(response_procedure_name: str,
                              session: Session = Depends(get_session)):
    db_response_procedure = response_procedure_repo.get_response_procedure(
        response_procedure_name=response_procedure_name, session=session)
    if not db_response_procedure:
        raise HTTPException(status_code=400, detail="ResponseProcedure name does not exist.")

    db_response_procedure = response_procedure_repo.delete_response_procedure(
        response_procedure_name=response_procedure_name, session=session)
    return db_response_procedure
