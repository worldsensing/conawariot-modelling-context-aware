from sqlmodel import Session, select

from app.schemas.procedure_type import ProcedureType


def get_procedure_type(procedure_type_name: str, session: Session):
    return session.exec(
        select(ProcedureType)
        .where(ProcedureType.name == procedure_type_name)
    ).first()


def get_procedure_types(offset: int, limit: int, session: Session):
    return session.exec(
        select(ProcedureType)
        .offset(offset).limit(limit)) \
        .all()


def create_procedure_type(procedure_type: ProcedureType,
                          session: Session):
    db_procedure_type = ProcedureType(
        name=procedure_type.name,
        procedure_type=procedure_type.procedure_type,
    )
    session.add(db_procedure_type)
    session.commit()
    session.refresh(db_procedure_type)
    return db_procedure_type


def delete_procedure_type(procedure_type_name: str, session: Session):
    procedure_type = get_procedure_type(procedure_type_name, session)
    session.delete(procedure_type)
    session.commit()
    return procedure_type
