from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.repository import procedure_type as procedure_type_repo
from app.schemas.procedure_type import ProcedureType

router = APIRouter(prefix="/procedure-types")


@router.get("/", response_model=List[ProcedureType])
def get_procedure_type_types(offset: int = 0, limit: int = Query(default=100, lte=100),
                             session: Session = Depends(get_session)):
    procedure_type_types = procedure_type_repo.get_procedure_types(
        offset=offset, limit=limit, session=session)
    return procedure_type_types


@router.post("/", response_model=ProcedureType)
def post_procedure_type(procedure_type: ProcedureType,
                        session: Session = Depends(get_session)):
    db_procedure_type = procedure_type_repo.get_procedure_type(
        procedure_type_name=procedure_type.name, session=session)
    if db_procedure_type:
        raise HTTPException(status_code=400, detail="ProcedureType name already registered")

    return procedure_type_repo.create_procedure_type(
        procedure_type=procedure_type, session=session)


@router.get("/{procedure_type_name}/", response_model=ProcedureType)
def get_procedure_type(procedure_type_name: str,
                       session: Session = Depends(get_session)):
    db_procedure_type = procedure_type_repo.get_procedure_type(
        procedure_type_name=procedure_type_name, session=session)
    if db_procedure_type is None:
        raise HTTPException(status_code=404, detail="ProcedureType not found")

    return db_procedure_type


@router.delete("/{procedure_type_name}/", response_model=ProcedureType)
def delete_procedure_type(procedure_type_name: str,
                          session: Session = Depends(get_session)):
    get_procedure_type(procedure_type_name=procedure_type_name,
                       session=session)

    db_procedure_type = procedure_type_repo.delete_procedure_type(
        procedure_type_name=procedure_type_name, session=session)
    return db_procedure_type
