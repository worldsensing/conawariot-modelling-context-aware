from database import session


def add_event_rule(event_rule):
    try:
        session.add(event_rule)
        session.flush()
        name = event_rule.name
        session.commit()
    except Exception as e:
        session.rollback()
        return None

    return name


def get_all_event_rules():
    from models.EventRule import EventRule

    try:
        event_rules = session.query(EventRule) \
            .all()
        session.commit()
    except:
        session.rollback()
        return None

    return event_rules


def get_event_rule(event_rule_name):
    from models.EventRule import EventRule

    try:
        event_rules = session.query(EventRule) \
            .filter_by(name=event_rule_name) \
            .first()
        session.commit()
    except:
        session.rollback()
        return None

    return event_rules


def update_event_rule(event_rule_name, event_rule):
    from models.EventRule import EventRule

    try:
        session.query(EventRule) \
            .filter_by(name=event_rule_name) \
            .update(event_rule)
        session.commit()
    except Exception as e:
        session.rollback()
        return None

    return event_rule_name


def delete_event_rule(event_rule_name):
    from models.EventRule import EventRule

    try:
        session.query(EventRule) \
            .filter_by(name=event_rule_name) \
            .delete()
        session.commit()
    except:
        session.rollback()
        return None

    return event_rule_name
