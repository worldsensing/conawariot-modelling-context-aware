from database import session


def add_observation(observation):
    try:
        session.add(observation)
        session.flush()
        id = observation.id
        session.commit()
    except:
        session.rollback()
        return None

    return id


def get_all_observations():
    from models.Observation import Observation

    observations = None
    try:
        observations = session.query(Observation) \
            .all()
        session.commit()
    except:
        session.rollback()

    return observations


def get_observation(observation_id):
    from models.Observation import Observation

    try:
        observation = session.query(Observation) \
            .filter_by(id=observation_id) \
            .first()
        session.commit()
    except:
        session.rollback()
        return None

    return observation


def delete_observation(observation_id):
    from models.Observation import Observation

    try:
        session.query(Observation) \
            .filter_by(id=observation_id) \
            .delete()
        session.commit()
    except:
        session.rollback()
        return None

    return observation_id


def get_observations_filter_sensor(sensor_name):
    from models.Observation import Observation

    try:
        observations = session.query(Observation) \
            .filter_by(sensor_name=sensor_name) \
            .all()
        session.commit()
    except:
        session.rollback()
        return None

    return observations
