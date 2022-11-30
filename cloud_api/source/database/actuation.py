from database import session


def add_actuation(actuation):
    try:
        session.add(actuation)
        session.flush()
        id = actuation.id
        session.commit()
    except:
        session.rollback()
        return None

    return id


def get_all_actuations():
    from models.Actuation import Actuation

    try:
        actuations = session.query(Actuation) \
            .all()
        session.commit()
    except:
        session.rollback()
        return None

    return actuations


def get_actuation(actuation_id):
    from models.Actuation import Actuation

    try:
        actuations = session.query(Actuation) \
            .filter_by(id=actuation_id) \
            .first()
        session.commit()
    except:
        session.rollback()
        return None

    return actuations


def update_actuation(actuation_id, actuation):
    from models.Actuation import Actuation

    try:
        session.query(Actuation) \
            .filter_by(id=actuation_id) \
            .update(actuation)
        session.commit()
    except Exception as e:
        session.rollback()
        return None

    return actuation_id


def delete_actuation(actuation_id):
    from models.Actuation import Actuation

    try:
        session.query(Actuation) \
            .filter_by(id=actuation_id) \
            .delete()
        session.commit()
    except:
        session.rollback()
        return None

    return actuation_id
