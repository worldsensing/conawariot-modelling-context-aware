import enum
from typing import Optional

from sqlmodel import Column, Enum, Field, SQLModel


class EventRuleTypeEnum(enum.Enum):
    SENSOR_SENSOR = "SENSOR_SENSOR"
    SENSOR_CONSTANT = "SENSOR_CONSTANT"


class EventRuleComparationTypeEnum(enum.Enum):
    EQUALS = "EQUALS"
    NOT_EQUALS = "NOT_EQUALS"
    LESS_THAN = "LESS_THAN"
    MORE_THAN = "MORE_THAN"
    MATH_ARITHMETIC_MEAN = "MATH_ARITHMETIC_MEAN"
    MATH_MEAN = "MATH_MEAN"
    MATH_MEDIAN = "MATH_MEDIAN"
    MATH_HARMONIC_MEAN = "MATH_HARMONIC_MEAN"
    MATH_STD_DEVIATION = "MATH_STD_DEVIATION"


class EventRuleValueTypeEnum(enum.Enum):
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"


class EventRuleType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)

    event_rule_type: EventRuleTypeEnum = Field(sa_column=Column(Enum(EventRuleTypeEnum)),
                                               nullable=False)
    event_rule_comparation_type: EventRuleComparationTypeEnum = Field(
        sa_column=Column(Enum(EventRuleComparationTypeEnum)), nullable=False)
    event_rule_value_type: EventRuleValueTypeEnum = Field(
        sa_column=Column(Enum(EventRuleValueTypeEnum)), nullable=False)
