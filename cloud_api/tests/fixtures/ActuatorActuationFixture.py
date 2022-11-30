from functools import partial

import factory

from models import ActuatorActuation
from .fixtures import dict_factory


class AbstractActuatorActuationFactory(factory.Factory):
    class Meta:
        model = ActuatorActuation
        abstract = True

    actuation_id = 0
    actuator_name = "Switch1"


class ActuatorActuationFactory(AbstractActuatorActuationFactory):
    pass


ActuatorActuationFactory._meta.exclude = ("id",)
ActuatorActuationDictFactory = partial(dict_factory, ActuatorActuationFactory)


class ActuatorActuationFactory2DB(AbstractActuatorActuationFactory,
                                  factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        sqlalchemy_session_persistence = "commit"
