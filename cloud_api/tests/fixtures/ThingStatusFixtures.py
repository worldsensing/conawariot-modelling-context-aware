from functools import partial

import factory

from models import ThingStatus
from .fixtures import dict_factory


class AbstractThingStatusFactory(factory.Factory):
    class Meta:
        model = ThingStatus
        abstract = True

    thing_name = "Thing1"
    platform_name = "Platform1"
    status = True


class ThingStatusFactory(AbstractThingStatusFactory):
    pass


ThingStatusFactory._meta.exclude = ("id",)
ThingStatusDictFactory = partial(dict_factory, ThingStatusFactory)


class ThingStatusFactory2DB(AbstractThingStatusFactory,
                            factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        sqlalchemy_session_persistence = "commit"
