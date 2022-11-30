from database import session


def add_event_rule_type(event_rule_type):
    try:
        session.add(event_rule_type)
        session.flush()
        name = event_rule_type.name
        session.commit()
    except Exception as e:
        session.rollback()
        return None

    return name


def get_all_event_rule_types():
    from models.EventRuleType import EventRuleType

    try:
        event_rule_types = session.query(EventRuleType) \
            .all()
        session.commit()
    except:
        session.rollback()
        return None

    return event_rule_types


def get_event_rule_type(event_rule_type_name):
    from models.EventRuleType import EventRuleType

    try:
        event_rule_types = session.query(EventRuleType) \
            .filter_by(name=event_rule_type_name) \
            .first()
        session.commit()
    except:
        session.rollback()
        return None

    return event_rule_types


def update_event_rule_type(event_rule_type_name, event_rule_type):
    from models.EventRuleType import EventRuleType

    try:
        session.query(EventRuleType) \
            .filter_by(name=event_rule_type_name) \
            .update(event_rule_type)
        session.commit()
    except Exception as e:
        session.rollback()
        return None

    return event_rule_type_name


def delete_event_rule_type(event_rule_type_name):
    from models.EventRuleType import EventRuleType

    try:
        session.query(EventRuleType) \
            .filter_by(name=event_rule_type_name) \
            .delete()
        session.commit()
    except:
        session.rollback()
        return None

    return event_rule_type_name
