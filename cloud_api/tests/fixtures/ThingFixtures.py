from functools import partial

import factory

from models import Thing
from .fixtures import dict_factory


class AbstractThingFactory(factory.Factory):
    class Meta:
        model = Thing
        abstract = True

    id = factory.Sequence(lambda n: int(n))
    name = "Arduino"
    type_name = "Inclinometer"
    location_name = None  # "MyLocation1"


class ThingFactory(AbstractThingFactory):
    pass


ThingFactory._meta.exclude = ("id",)
ThingDictFactory = partial(dict_factory, ThingFactory)


class ThingFactory2DB(AbstractThingFactory, factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        sqlalchemy_session_persistence = "commit"
