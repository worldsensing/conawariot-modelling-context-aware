from sqlmodel import Session, select

from app.schemas.thing import Thing


def get_thing(thing_name: str, session: Session):
    return session.exec(
        select(Thing)
        .where(Thing.name == thing_name)
    ).first()


def get_things(offset: int, limit: int, session: Session):
    return session.exec(
        select(Thing)
        .offset(offset).limit(limit)
    ).all()


def create_thing(thing: Thing, session: Session):
    db_thing = Thing(
        name=thing.name,
        active=thing.active,
        location_name=thing.location_name,
        info=thing.info,
        group_name=thing.group_name,
        gateway_name=thing.gateway_name,
        sampling_rate=thing.sampling_rate,
        lastConnectTime=thing.lastConnectTime,
        lastDisconnectTime=thing.lastDisconnectTime,
        lastActivityTime=thing.lastActivityTime,
        inactivityAlarmTime=thing.inactivityAlarmTime
    )
    session.add(db_thing)
    session.commit()
    session.refresh(db_thing)
    return db_thing


def delete_thing(thing_name: str, session: Session):
    thing = get_thing(thing_name, session)
    session.delete(thing)
    session.commit()
    return thing
