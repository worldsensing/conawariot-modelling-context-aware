from typing import Optional

from sqlmodel import Field, SQLModel


class ResponseProcedure(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)

    # Relations
    # TODO This should be a list, now we assume is One-to-Many, should be Many-to-Many
    context_aware_rule_name: str = Field(nullable=False, foreign_key="contextawarerule.name")
    # TODO Add FK, not working, foreign_key="proceduretype.name")
    procedure_type_name: str = Field(nullable=False)
    # TODO This should be a list
    actuator_name: str = Field(nullable=False, foreign_key="actuator.name")
    #
