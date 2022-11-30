from database import session


def add_location(location):
    try:
        session.add(location)
        session.flush()
        name = location.name
        session.commit()
    except:
        session.rollback()
        return None

    return name


def get_all_locations():
    from models.Location import Location

    try:
        locations = session.query(Location) \
            .all()
        session.commit()
    except:
        session.rollback()
        return None

    return locations


def get_location(location_name):
    from models.Location import Location

    try:
        locations = session.query(Location) \
            .filter_by(name=location_name) \
            .first()
        session.commit()
    except:
        session.rollback()
        return None

    return locations


def update_location(location_name, location):
    from models.Location import Location

    try:
        session.query(Location) \
            .filter_by(name=location_name) \
            .update(location)
        session.commit()
    except Exception as e:
        session.rollback()
        return None

    return location_name


def delete_location(location_name):
    from models.Location import Location

    try:
        session.query(Location) \
            .filter_by(name=location_name) \
            .delete()
        session.commit()
    except:
        session.rollback()
        return None

    return location_name
