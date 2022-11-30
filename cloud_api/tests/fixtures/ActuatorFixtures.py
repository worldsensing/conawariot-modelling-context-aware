from functools import partial

import factory

from models import Actuator
from .fixtures import dict_factory


class AbstractActuatorFactory(factory.Factory):
    class Meta:
        model = Actuator
        abstract = True

    id = factory.Sequence(lambda n: int(n))
    thing_name = "ODroid1"
    name = "Switch"
    actuatable_property_name = "LightInRoom2"
    location_name = "MyLocation1"


class ActuatorFactory(AbstractActuatorFactory):
    pass


ActuatorFactory._meta.exclude = ("id",)
ActuatorDictFactory = partial(dict_factory, ActuatorFactory)


class ActuatorFactory2DB(AbstractActuatorFactory,
                         factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        sqlalchemy_session_persistence = "commit"
