from database import session


def add_context_aware_rule(context_aware_rule):
    try:
        session.add(context_aware_rule)
        session.flush()
        name = context_aware_rule.name
        session.commit()
    except Exception as e:
        session.rollback()
        return None

    return name


def get_all_context_aware_rules():
    from models.ContextAwareRule import ContextAwareRule

    try:
        context_aware_rules = session.query(ContextAwareRule) \
            .all()
        session.commit()
    except:
        session.rollback()
        return None

    return context_aware_rules


def get_context_aware_rule(context_aware_rule_name):
    from models.ContextAwareRule import ContextAwareRule

    try:
        context_aware_rules = session.query(ContextAwareRule) \
            .filter_by(name=context_aware_rule_name) \
            .first()
        session.commit()
    except:
        session.rollback()
        return None

    return context_aware_rules


def update_context_aware_rule(context_aware_rule_name, context_aware_rule):
    from models.ContextAwareRule import ContextAwareRule

    try:
        session.query(ContextAwareRule) \
            .filter_by(name=context_aware_rule_name) \
            .update(context_aware_rule)
        session.commit()
    except Exception as e:
        session.rollback()
        return None

    return context_aware_rule_name


def delete_context_aware_rule(context_aware_rule_name):
    from models.ContextAwareRule import ContextAwareRule

    try:
        session.query(ContextAwareRule) \
            .filter_by(name=context_aware_rule_name) \
            .delete()
        session.commit()
    except:
        session.rollback()
        return None

    return context_aware_rule_name
