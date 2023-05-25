from sqlmodel import Session, select

from app.schemas.event_rule_type import EventRuleType


def get_event_rule_type(event_rule_type_name: str, session: Session):
    return session.exec(
        select(EventRuleType)
        .where(EventRuleType.name == event_rule_type_name)
    ).first()


def get_event_rule_types(offset: int, limit: int, session: Session):
    return session.exec(
        select(EventRuleType)
        .offset(offset).limit(limit)) \
        .all()


def create_event_rule_type(event_rule_type: EventRuleType, session: Session):
    db_event_rule_type = EventRuleType(
        name=event_rule_type.name,
        event_rule_type=event_rule_type.event_rule_type,
        event_rule_comparation_type=event_rule_type.event_rule_comparation_type,
        event_rule_value_type=event_rule_type.event_rule_value_type
    )
    session.add(db_event_rule_type)
    session.commit()
    session.refresh(db_event_rule_type)
    return db_event_rule_type


def delete_event_rule_type(event_rule_type_name: str, session: Session):
    event_rule_type = get_event_rule_type(event_rule_type_name, session)
    session.delete(event_rule_type)
    session.commit()
    return event_rule_type
