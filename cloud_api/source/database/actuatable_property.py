from database import session


def add_actuatable_property(actuatable_property):
    try:
        session.add(actuatable_property)
        session.flush()
        name = actuatable_property.name
        session.commit()
    except:
        session.rollback()
        return None

    return name


def get_all_actuatable_properties():
    from models.ActuatableProperty import ActuatableProperty

    try:
        actuatable_properties = session.query(ActuatableProperty) \
            .all()
        session.commit()
    except:
        session.rollback()
        return None

    return actuatable_properties


def get_actuatable_property(actuatable_property_name):
    from models.ActuatableProperty import ActuatableProperty

    try:
        actuatable_properties = session.query(ActuatableProperty) \
            .filter_by(name=actuatable_property_name) \
            .first()
        session.commit()
    except:
        session.rollback()
        return None

    return actuatable_properties


def update_actuatable_property(actuatable_property_name, actuatable_property):
    from models.ActuatableProperty import ActuatableProperty

    try:
        session.query(ActuatableProperty) \
            .filter_by(name=actuatable_property_name) \
            .update(actuatable_property)
        session.commit()
    except Exception as e:
        session.rollback()
        return None

    return actuatable_property_name


def delete_actuatable_property(actuatable_property_name):
    from models.ActuatableProperty import ActuatableProperty

    try:
        session.query(ActuatableProperty) \
            .filter_by(name=actuatable_property_name) \
            .delete()
        session.commit()
    except:
        session.rollback()
        return None

    return actuatable_property_name
