from functools import partial

import factory

from models import ActuatableProperty
from .fixtures import dict_factory


class AbstractActuatablePropertyFactory(factory.Factory):
    class Meta:
        model = ActuatableProperty
        abstract = True

    id = factory.Sequence(lambda n: int(n))
    name = "Leg1"
    feature_of_interest_name = "Person1"


class ActuatablePropertyFactory(AbstractActuatablePropertyFactory):
    pass


ActuatablePropertyFactory._meta.exclude = ("id",)
ActuatablePropertyDictFactory = partial(dict_factory, ActuatablePropertyFactory)


class ActuatablePropertyFactory2DB(AbstractActuatablePropertyFactory,
                                   factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        sqlalchemy_session_persistence = "commit"
