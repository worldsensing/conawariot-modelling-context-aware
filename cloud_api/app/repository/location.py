from sqlmodel import Session, select

from app.schemas.location import Location


def get_location(location_name: str, session: Session):
    return session.exec(
        select(Location)
        .where(Location.name == location_name)
    ).first()


def get_locations(offset: int, limit: int, session: Session):
    return session.exec(
        select(Location)
        .offset(offset).limit(limit)) \
        .all()


def create_location(location: Location, session: Session):
    db_location = Location(
        name=location.name,
        geo_feature=location.geo_feature,
        geo_coordinates=location.geo_coordinates
    )
    session.add(db_location)
    session.commit()
    session.refresh(db_location)
    return db_location


def delete_location(location_name: str, session: Session):
    location = get_location(location_name, session)
    session.delete(location)
    session.commit()
    return location
