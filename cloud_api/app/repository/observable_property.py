from sqlmodel import Session, select

from app.schemas.observable_property import ObservableProperty


def get_observable_property(observable_property_name: str, session: Session):
    return session.exec(
        select(ObservableProperty)
        .where(ObservableProperty.name == observable_property_name)
    ).first()


def get_observable_properties(offset: int, limit: int, session: Session):
    return session.exec(
        select(ObservableProperty)
        .offset(offset).limit(limit)) \
        .all()


def create_observable_property(observable_property: ObservableProperty, session: Session):
    db_observable_property = ObservableProperty(
        name=observable_property.name,
        type_of_observation=observable_property.type_of_observation,
        feature_of_interest_name=observable_property.feature_of_interest_name
    )
    session.add(db_observable_property)
    session.commit()
    session.refresh(db_observable_property)
    return db_observable_property


def delete_observable_property(observable_property_name: str, session: Session):
    observable_property = get_observable_property(observable_property_name, session)
    session.delete(observable_property)
    session.commit()
    return observable_property
