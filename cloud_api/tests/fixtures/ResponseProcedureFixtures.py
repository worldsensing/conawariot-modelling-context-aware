from functools import partial

import factory

from models import ResponseProcedure
from .fixtures import dict_factory


class AbstractResponseProcedureFactory(factory.Factory):
    class Meta:
        model = ResponseProcedure
        abstract = True

    id = factory.Sequence(lambda n: int(n))
    name = "Rule1"
    context_aware_rule_name = "BR1"
    procedure_type_name = "PRTY1"
    actuator_name = "ACTUATOR1"


class ResponseProcedureFactory(AbstractResponseProcedureFactory):
    pass


ResponseProcedureFactory._meta.exclude = ("id",)
ResponseProcedureDictFactory = partial(dict_factory, ResponseProcedureFactory)


class ResponseProcedureFactory2DB(AbstractResponseProcedureFactory,
                                  factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        sqlalchemy_session_persistence = "commit"
