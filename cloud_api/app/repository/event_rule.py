from sqlmodel import Session, select

from app.schemas.event_rule import EventRule


def get_event_rule(event_rule_name: str, session: Session):
    return session.exec(
        select(EventRule)
        .where(EventRule.name == event_rule_name)
    ).first()


def get_event_rules(offset: int, limit: int, session: Session):
    return session.exec(
        select(EventRule)
        .offset(offset).limit(limit)) \
        .all()


def create_event_rule(event_rule: EventRule, session: Session):
    db_event_rule = EventRule(
        name=event_rule.name,
        event_rule_type_name=event_rule.event_rule_type_name,
        context_aware_rule_name=event_rule.context_aware_rule_name,
        sensor_1_name=event_rule.sensor_1_name,
        sensor_2_name=event_rule.sensor_2_name,
        value_to_compare_boolean=event_rule.value_to_compare_boolean,
        value_to_compare_string=event_rule.value_to_compare_string,
        value_to_compare_integer=event_rule.value_to_compare_integer,
        value_to_compare_float=event_rule.value_to_compare_float
    )
    session.add(db_event_rule)
    session.commit()
    session.refresh(db_event_rule)
    return db_event_rule


def delete_event_rule(event_rule_name: str, session: Session):
    event_rule = get_event_rule(event_rule_name, session)
    session.delete(event_rule)
    session.commit()
    return event_rule
