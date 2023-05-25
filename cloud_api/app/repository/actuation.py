from sqlmodel import Session, select

from app.schemas.actuation import Actuation


# TODO This EXEC can be changed without where
def get_actuation(actuation_id: int, session: Session):
    return session.exec(
        select(Actuation)
        .where(Actuation.id == actuation_id)
    ).first()


def get_actuations(offset: int, limit: int, session: Session):
    return session.exec(
        select(Actuation)
        .offset(offset).limit(limit)) \
        .all()


def create_actuation(actuation: Actuation, session: Session):
    db_actuation = Actuation(
        time_start=actuation.time_start,
        time_end=actuation.time_end,
        actuator_name=actuation.actuator_name,
        actuatable_property_name=actuation.actuatable_property_name
    )
    session.add(db_actuation)
    session.commit()
    session.refresh(db_actuation)
    return db_actuation


def delete_actuation(actuation_id: int, session: Session):
    actuation = get_actuation(actuation_id, session)
    session.delete(actuation)
    session.commit()
    return actuation
