from database import session


def add_thing(thing):
    try:
        session.add(thing)
        session.flush()
        name = thing.name
        session.commit()
    except:
        session.rollback()
        return None

    return name


def get_all_things():
    from models.Thing import Thing

    try:
        things = session.query(Thing) \
            .all()
        session.commit()
    except:
        session.rollback()
        return None

    return things


def get_thing(thing_name):
    from models.Thing import Thing

    try:
        thing = session.query(Thing) \
            .filter_by(name=thing_name) \
            .first()
        session.commit()
    except:
        session.rollback()
        return None

    return thing


def update_thing(thing_name, thing):
    from models.Thing import Thing

    try:
        session.query(Thing) \
            .filter_by(name=thing_name) \
            .update(thing)
        session.commit()
    except:
        session.rollback()
        return None

    return thing_name


def delete_thing(thing_name):
    from models.Thing import Thing

    try:
        session.query(Thing) \
            .filter_by(name=thing_name) \
            .delete()
        session.commit()
    except:
        session.rollback()
        return None

    return thing_name


def get_things_filter_thing_type(thing_type):
    from models.Thing import Thing

    try:
        things = session.query(Thing) \
            .filter_by(type=thing_type) \
            .all()
        session.commit()
    except:
        session.rollback()
        return None

    return things
