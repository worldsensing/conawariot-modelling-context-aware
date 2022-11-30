from database import session


def add_condition_rule(condition_rule):
    try:
        session.add(condition_rule)
        session.flush()
        name = condition_rule.name
        session.commit()
    except Exception as e:
        session.rollback()
        return None

    return name


def get_all_condition_rules():
    from models.ConditionRule import ConditionRule

    try:
        condition_rules = session.query(ConditionRule) \
            .all()
        session.commit()
    except:
        session.rollback()
        return None

    return condition_rules


def get_condition_rule(condition_rule_name):
    from models.ConditionRule import ConditionRule

    try:
        condition_rules = session.query(ConditionRule) \
            .filter_by(name=condition_rule_name) \
            .first()
        session.commit()
    except:
        session.rollback()
        return None

    return condition_rules


def update_condition_rule(condition_rule_name, condition_rule):
    from models.ConditionRule import ConditionRule

    try:
        session.query(ConditionRule) \
            .filter_by(name=condition_rule_name) \
            .update(condition_rule)
        session.commit()
    except Exception as e:
        session.rollback()
        return None

    return condition_rule_name


def delete_condition_rule(condition_rule_name):
    from models.ConditionRule import ConditionRule

    try:
        session.query(ConditionRule) \
            .filter_by(name=condition_rule_name) \
            .delete()
        session.commit()
    except:
        session.rollback()
        return None

    return condition_rule_name
