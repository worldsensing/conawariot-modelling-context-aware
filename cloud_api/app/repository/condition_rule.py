from sqlmodel import Session, select

from app.schemas.condition_rule import ConditionRule


def get_condition_rule(condition_rule_name: str, session: Session):
    return session.exec(
        select(ConditionRule)
        .where(ConditionRule.name == condition_rule_name)
    ).first()


def get_condition_rules(offset: int, limit: int, session: Session):
    return session.exec(
        select(ConditionRule)
        .offset(offset).limit(limit)) \
        .all()


def create_condition_rule(condition_rule: ConditionRule, session: Session):
    db_condition_rule = ConditionRule(
        name=condition_rule.name,
        context_aware_rule_name=condition_rule.context_aware_rule_name,
        event_rule_1_name=condition_rule.event_rule_1_name,
        event_rule_2_name=condition_rule.event_rule_2_name,
        condition_rule_1_name=condition_rule.condition_rule_1_name,
        condition_rule_2_name=condition_rule.condition_rule_2_name,
        condition_comparation_type=condition_rule.condition_comparation_type
    )
    session.add(db_condition_rule)
    session.commit()
    session.refresh(db_condition_rule)
    return db_condition_rule


def delete_condition_rule(condition_rule_name: str, session: Session):
    condition_rule = get_condition_rule(condition_rule_name, session)
    session.delete(condition_rule)
    session.commit()
    return condition_rule
