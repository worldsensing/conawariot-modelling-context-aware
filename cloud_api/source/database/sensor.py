from database import session


def add_sensor(sensor):
    try:
        session.add(sensor)
        session.flush()
        name = sensor.name
        session.commit()
    except:
        session.rollback()
        return None

    return name


def get_all_sensors():
    from models.Sensor import Sensor

    try:
        sensors = session.query(Sensor) \
            .all()
        session.commit()
    except:
        session.rollback()
        return None

    return sensors


def get_sensor(sensor_name):
    from models.Sensor import Sensor

    try:
        sensor = session.query(Sensor) \
            .filter_by(name=sensor_name) \
            .first()
        session.commit()
    except:
        session.rollback()
        return None

    return sensor


def update_sensor(sensor_name, sensor):
    from models.Sensor import Sensor

    try:
        session.query(Sensor) \
            .filter_by(name=sensor_name) \
            .update(sensor)
        session.commit()
    except:
        session.rollback()
        return None

    return sensor_name


def delete_sensor(sensor_name):
    from models.Sensor import Sensor

    try:
        session.query(Sensor) \
            .filter_by(name=sensor_name) \
            .delete()
        session.commit()
    except:
        session.rollback()
        return None

    return sensor_name


def get_sensors_filter_sensor_type(sensor_type):
    from models.Sensor import Sensor

    try:
        sensors = session.query(Sensor) \
            .filter_by(type=sensor_type) \
            .all()
        session.commit()
    except:
        session.rollback()
        return None

    return sensors
