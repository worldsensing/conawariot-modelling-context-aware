from sqlmodel import Session, select

from app.schemas.observation import Observation


# TODO Check if can be done more straight without select
def get_observation_id(observation_id: int, session: Session):
    return session.exec(
        select(Observation)
        .where(Observation.id == observation_id)
    ).first()


def get_observations_sensor(sensor_name: str, offset: int, limit: int, session: Session):
    return session.exec(
        select(Observation)
        .where(Observation.sensor_name == sensor_name)
        .offset(offset).limit(limit)
    ).all()


def get_observations(offset: int, limit: int, session: Session):
    return session.exec(
        select(Observation)
        .offset(offset).limit(limit)
    ).all()


def create_observation(observation: Observation, session: Session):
    db_observation = Observation(
        time_start=observation.time_start,
        sensor_name=observation.sensor_name,
        observable_property_name=observation.observable_property_name,
        time_end=observation.time_end,
        value_int=observation.value_int,
        value_float=observation.value_float,
        value_str=observation.value_str,
        value_bool=observation.value_bool
    )
    session.add(db_observation)
    session.commit()
    session.refresh(db_observation)
    return db_observation


def delete_observations_sensor(sensor_name: str, session: Session):
    offset = 0  # TODO Improve
    limit = 100  # TODO Improve
    observations_sensor = get_observations_sensor(sensor_name, offset=offset, limit=limit,
                                                  session=session)
    for observation_sensor in observations_sensor:
        session.delete(observation_sensor)
        session.commit()
    return observations_sensor


def delete_observation_id(observation_id: int, session: Session):
    observation_sensor = get_observation_id(observation_id, session)
    session.delete(observation_sensor)
    session.commit()
    return observation_sensor
