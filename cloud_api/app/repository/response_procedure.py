from sqlmodel import Session, select

from app.schemas.response_procedure import ResponseProcedure


def get_response_procedure(response_procedure_name: str, session: Session):
    return session.exec(
        select(ResponseProcedure)
        .where(ResponseProcedure.name == response_procedure_name)
    ).first()


def get_response_procedures(offset: int, limit: int, session: Session):
    return session.exec(
        select(ResponseProcedure)
        .offset(offset).limit(limit)) \
        .all()


def create_response_procedure(response_procedure: ResponseProcedure, session: Session):
    db_response_procedure = ResponseProcedure(
        name=response_procedure.name,
        context_aware_rule_name=response_procedure.context_aware_rule_name,
        procedure_type_name=response_procedure.procedure_type_name,
        actuator_name=response_procedure.actuator_name
    )
    session.add(db_response_procedure)
    session.commit()
    session.refresh(db_response_procedure)
    return db_response_procedure


def delete_response_procedure(response_procedure_name: str, session: Session):
    response_procedure = get_response_procedure(response_procedure_name, session)
    session.delete(response_procedure)
    session.commit()
    return response_procedure
