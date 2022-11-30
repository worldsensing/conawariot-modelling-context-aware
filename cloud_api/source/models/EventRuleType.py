# -*- coding: utf-8 -*-
import enum

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from database import Base


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


class EventRuleType(Base):
    __tablename__ = "event_rule_type"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(32), unique=True, nullable=False)
    event_rule_type = Column(Enum(EventRuleTypeEnum), nullable=False)
    event_rule_comparation_type = Column(Enum(EventRuleComparationTypeEnum), nullable=False)
    event_rule_value_type = Column(Enum(EventRuleValueTypeEnum))

    event_rules = relationship('EventRule')

    def __str__(self):
        event_rule_value_type = self.event_rule_value_type.value \
            if self.event_rule_value_type is not None else None

        return f"{self.id}, {self.name}, {self.event_rule_type.value}, " \
               f"{self.event_rule_comparation_type.value}, " \
               f"{event_rule_value_type}, " \
               f"{self.event_rules}"
