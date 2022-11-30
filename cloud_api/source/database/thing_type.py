from database import session


def add_thing_type(thing_type):
    try:
        session.add(thing_type)
        session.flush()
        name = thing_type.name
        session.commit()
    except:
        session.rollback()
        return None

    return name


def get_all_thing_types():
    from models.ThingType import ThingType

    try:
        thing_types = session.query(ThingType) \
            .all()
        session.commit()
    except:
        session.rollback()
        return None

    return thing_types


def get_thing_type(thing_type_name):
    from models.ThingType import ThingType

    try:
        thing_types = session.query(ThingType) \
            .filter_by(name=thing_type_name) \
            .first()
        session.commit()
    except:
        session.rollback()
        return None

    return thing_types


def update_thing_type(thing_type_name, thing_type):
    from models.ThingType import ThingType

    try:
        session.query(ThingType) \
            .filter_by(name=thing_type_name) \
            .update(thing_type)
        session.commit()
    except:
        session.rollback()
        return None

    return thing_type_name


def delete_thing_type(thing_type_name):
    from models.ThingType import ThingType

    try:
        session.query(ThingType) \
            .filter_by(name=thing_type_name) \
            .delete()
        session.commit()
    except:
        session.rollback()
        return None

    return thing_type_name
