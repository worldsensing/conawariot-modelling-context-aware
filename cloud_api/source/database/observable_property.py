from database import session


def add_observable_property(observable_property):
    try:
        session.add(observable_property)
        session.flush()
        name = observable_property.name
        session.commit()
    except:
        session.rollback()
        return None

    return name


def get_all_observable_properties():
    from models.ObservableProperty import ObservableProperty

    try:
        observable_properties = session.query(ObservableProperty) \
            .all()
        session.commit()
    except:
        session.rollback()
        return None

    return observable_properties


def get_observable_property(observable_property_name):
    from models.ObservableProperty import ObservableProperty

    try:
        observable_properties = session.query(ObservableProperty) \
            .filter_by(name=observable_property_name) \
            .first()
        session.commit()
    except:
        session.rollback()
        return None

    return observable_properties


def update_observable_property(observable_property_name, observable_property):
    from models.ObservableProperty import ObservableProperty

    try:
        session.query(ObservableProperty) \
            .filter_by(name=observable_property_name) \
            .update(observable_property)
        session.commit()
    except Exception as e:
        session.rollback()
        return None

    return observable_property_name


def delete_observable_property(observable_property_name):
    from models.ObservableProperty import ObservableProperty

    try:
        session.query(ObservableProperty) \
            .filter_by(name=observable_property_name) \
            .delete()
        session.commit()
    except:
        session.rollback()
        return None

    return observable_property_name
