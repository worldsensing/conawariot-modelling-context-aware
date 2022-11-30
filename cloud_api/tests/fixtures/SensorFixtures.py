from functools import partial

import factory

from models import Sensor
from .fixtures import dict_factory


class AbstractSensorFactory(factory.Factory):
    class Meta:
        model = Sensor
        abstract = True

    id = factory.Sequence(lambda n: int(n))
    thing_name = "RaspberryA"
    name = "RainSensorA"
    location_name = None  # "MyLocation1"


class SensorFactory(AbstractSensorFactory):
    pass


SensorFactory._meta.exclude = ("id",)
SensorDictFactory = partial(dict_factory, SensorFactory)


class SensorFactory2DB(AbstractSensorFactory, factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        sqlalchemy_session_persistence = "commit"
