from functools import partial

import factory

from models import Location
from .fixtures import dict_factory


class AbstractLocationFactory(factory.Factory):
    class Meta:
        model = Location
        abstract = True

    id = factory.Sequence(lambda n: int(n))
    name = "Location1"
    latlng = None  # "41.2, 2.1"


class LocationFactory(AbstractLocationFactory):
    pass


LocationFactory._meta.exclude = ("id",)
LocationDictFactory = partial(dict_factory, LocationFactory)


class LocationFactory2DB(AbstractLocationFactory, factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        sqlalchemy_session_persistence = "commit"
