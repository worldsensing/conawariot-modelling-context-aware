from functools import partial

import factory

from models import Platform
from .fixtures import dict_factory


class AbstractPlatformFactory(factory.Factory):
    class Meta:
        model = Platform
        abstract = True

    id = factory.Sequence(lambda n: int(n))
    name = "Car"
    location_name = None


class PlatformFactory(AbstractPlatformFactory):
    pass


PlatformFactory._meta.exclude = ("id",)
PlatformDictFactory = partial(dict_factory, PlatformFactory)


class PlatformFactory2DB(AbstractPlatformFactory, factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        sqlalchemy_session_persistence = "commit"
