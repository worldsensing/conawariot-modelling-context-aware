from sqlmodel import Session, select

from app.schemas.group import Group


def get_group(group_name: str, session: Session):
    return session.exec(
        select(Group)
        .where(Group.name == group_name)
    ).first()


def get_groups(offset, limit, session: Session):
    return session.query(Group).offset(offset).limit(limit).all()


def create_group(group: Group, session: Session):
    db_group = Group(
        name=group.name,
        location_name=group.location_name,
        thing_name=group.thing_name,
        gateway_name=group.gateway_name,
    )
    session.add(db_group)
    session.commit()
    session.refresh(db_group)
    return db_group


def delete_group(group_name: str, session: Session):
    group = get_group(group_name, session)
    session.delete(group)
    session.commit()
    return group
