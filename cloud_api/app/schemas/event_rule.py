from typing import Optional

from sqlmodel import Field, SQLModel


class EventRule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)

    value_to_compare_integer: Optional[int] = Field()
    value_to_compare_boolean: Optional[bool] = Field()
    value_to_compare_string: Optional[str] = Field()
    value_to_compare_float: Optional[float] = Field()

    # Relations
    # TODO This should be a list, now we assume is One-to-Many, should be Many-to-Many
    context_aware_rule_name: str = Field(nullable=False, foreign_key="contextawarerule.name")
    event_rule_type_name: str = Field(nullable=False, foreign_key="eventruletype.name")
    sensor_1_name: str = Field(nullable=False, foreign_key="sensor.name")
    sensor_2_name: Optional[str] = Field(foreign_key="sensor.name")
    # TODO Add relation to ConditionRule?
    #
