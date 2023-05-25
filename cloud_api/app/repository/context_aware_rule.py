from sqlmodel import Session, select

from app.schemas.context_aware_rule import ContextAwareRule


def get_context_aware_rule(context_aware_rule_name: str, session: Session):
    return session.exec(
        select(ContextAwareRule)
        .where(ContextAwareRule.name == context_aware_rule_name)
    ).first()


def get_context_aware_rules(offset: int, limit: int, session: Session):
    return session.exec(
        select(ContextAwareRule)
        .offset(offset).limit(limit)) \
        .all()


def create_context_aware_rule(context_aware_rule: ContextAwareRule, session: Session):
    db_context_aware_rule = ContextAwareRule(
        name=context_aware_rule.name,
        executing=context_aware_rule.executing,
    )
    session.add(db_context_aware_rule)
    session.commit()
    session.refresh(db_context_aware_rule)
    return db_context_aware_rule


def delete_context_aware_rule(context_aware_rule_name: str, session: Session):
    context_aware_rule = get_context_aware_rule(context_aware_rule_name, session)
    session.delete(context_aware_rule)
    session.commit()
    return context_aware_rule
