from database import session


def add_actuator(actuator):
    try:
        session.add(actuator)
        session.flush()
        name = actuator.name
        session.commit()
    except:
        session.rollback()
        return None

    return name


def get_all_actuators():
    from models.Actuator import Actuator

    try:
        actuators = session.query(Actuator) \
            .all()
        session.commit()
    except:
        session.rollback()
        return None

    return actuators


def get_actuator(actuator_name):
    from models.Actuator import Actuator

    try:
        actuators = session.query(Actuator) \
            .filter_by(name=actuator_name) \
            .first()
        session.commit()
    except:
        session.rollback()
        return None

    return actuators


def update_actuator(actuator_name, actuator):
    from models.Actuator import Actuator

    try:
        session.query(Actuator) \
            .filter_by(name=actuator_name) \
            .update(actuator)
        session.commit()
    except Exception as e:
        session.rollback()
        return None

    return actuator_name


def delete_actuator(actuator_name):
    from models.Actuator import Actuator

    try:
        session.query(Actuator) \
            .filter_by(name=actuator_name) \
            .delete()
        session.commit()
    except:
        session.rollback()
        return None

    return actuator_name
