from functools import partial

import factory

from models import ThingType
from .fixtures import dict_factory


class AbstractThingTypeFactory(factory.Factory):
    class Meta:
        model = ThingType
        abstract = True

    id = factory.Sequence(lambda n: int(n))
    name = "Inclinometer"


class ThingTypeFactory(AbstractThingTypeFactory):
    pass


ThingTypeFactory._meta.exclude = ("id",)
ThingTypeDictFactory = partial(dict_factory, ThingTypeFactory)


class ThingTypeFactory2DB(AbstractThingTypeFactory,
                          factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        sqlalchemy_session_persistence = "commit"
