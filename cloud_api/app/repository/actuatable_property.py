from sqlmodel import Session, select

from app.schemas.actuatable_property import ActuatableProperty


def get_actuatable_property(actuatable_property_name: str, session: Session):
    return session.exec(
        select(ActuatableProperty)
        .where(ActuatableProperty.name == actuatable_property_name)
    ).first()


def get_actuatable_properties(offset: int, limit: int, session: Session):
    return session.exec(
        select(ActuatableProperty)
        .offset(offset).limit(limit)) \
        .all()


def create_actuatable_property(actuatable_property: ActuatableProperty, session: Session):
    db_actuatable_property = ActuatableProperty(
        name=actuatable_property.name,
        feature_of_interest_name=actuatable_property.feature_of_interest_name
    )
    session.add(db_actuatable_property)
    session.commit()
    session.refresh(db_actuatable_property)
    return db_actuatable_property


def delete_actuatable_property(actuatable_property_name: str, session: Session):
    actuatable_property = get_actuatable_property(actuatable_property_name, session)
    session.delete(actuatable_property)
    session.commit()
    return actuatable_property
