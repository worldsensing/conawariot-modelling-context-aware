from typing import Optional, List

from sqlmodel import Field, SQLModel, Relationship

from app.schemas.condition_rule import ConditionRule
from app.schemas.event_rule import EventRule
from app.schemas.response_procedure import ResponseProcedure


class ContextAwareRule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)

    executing: bool = Field(default=False)

    # Relations
    # TODO Now we assume is Many-to-One, should be Many-to-Many
    event_rules: List["EventRule"] = Relationship()
    condition_rules: List["ConditionRule"] = Relationship()
    response_procedures: List["ResponseProcedure"] = Relationship()
    #
