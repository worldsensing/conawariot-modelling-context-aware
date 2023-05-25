from sqlmodel import Session, select

from app.schemas.actuator import Actuator


def get_actuator(actuator_name: str, session: Session):
    return session.exec(
        select(Actuator)
        .where(Actuator.name == actuator_name)
    ).first()


def get_actuators(offset: int, limit: int, session: Session):
    return session.exec(
        select(Actuator)
        .offset(offset).limit(limit)) \
        .all()


def create_actuator(actuator: Actuator, session: Session):
    db_actuator = Actuator(
        name=actuator.name,
        thing_name=actuator.thing_name,
        actuatable_property_name=actuator.actuatable_property_name,
        location_name=actuator.location_name,
        info=actuator.info,
        response_procedure_name=actuator.response_procedure_name,
        lastConnectTime=actuator.lastConnectTime,
        lastDisconnectTime=actuator.lastDisconnectTime,
        lastActivityTime=actuator.lastActivityTime,
        inactivityAlarmTime=actuator.inactivityAlarmTime
    )
    session.add(db_actuator)
    session.commit()
    session.refresh(db_actuator)
    return db_actuator


def delete_actuator(actuator_name: str, session: Session):
    actuator = get_actuator(actuator_name, session)
    session.delete(actuator)
    session.commit()
    return actuator
