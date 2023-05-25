from sqlmodel import Session, select

from app.schemas.sensor import Sensor


def get_sensor(sensor_name: str, session: Session):
    return session.exec(
        select(Sensor)
        .where(Sensor.name == sensor_name)
    ).first()


def get_sensors(offset: int, limit: int, session: Session):
    return session.exec(
        select(Sensor)
        .offset(offset).limit(limit)
    ).all()


def get_sensors_by_observable_property(observable_property_name: str, offset: int, limit: int,
                                       session: Session):
    return session.exec(
        select(Sensor)
        .where(Sensor.observable_property_name == observable_property_name)
        .offset(offset).limit(limit)
    ).all()


def create_sensor(sensor: Sensor, session: Session):
    db_sensor = Sensor(
        name=sensor.name,
        active=sensor.active,
        observable_property_name=sensor.observable_property_name,
        location_name=sensor.location_name,
        info=sensor.info,
        thing_name=sensor.thing_name,
        gateway_name=sensor.gateway_name,
        lastConnectTime=sensor.lastConnectTime,
        lastDisconnectTime=sensor.lastDisconnectTime,
        lastActivityTime=sensor.lastActivityTime,
        inactivityAlarmTime=sensor.inactivityAlarmTime
    )
    session.add(db_sensor)
    session.commit()
    session.refresh(db_sensor)
    return db_sensor


def delete_sensor(sensor_name: str, session: Session):
    sensor = get_sensor(sensor_name, session)
    session.delete(sensor)
    session.commit()
    return sensor
