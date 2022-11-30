# -*- coding: utf-8 -*-
import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from database import Base


class ObservableValueTypeEnum(enum.Enum):
    value_boolean = "BOOLEAN"
    value_string = "STRING"
    value_integer = "INTEGER"
    value_float = "FLOAT"


class ObservableProperty(Base):
    __tablename__ = "observable_property"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(32), unique=True, nullable=False)
    value_type_to_measure = Column(Enum(ObservableValueTypeEnum), nullable=False)
    feature_of_interest_name = Column(String(32),
                                      ForeignKey("feature_of_interest.name", ondelete="cascade"))
    sensors = relationship("Sensor")

    # Add enums?

    def __str__(self):
        return f"{self.id}, {self.name}, {self.value_type_to_measure.value}, " \
               f"{self.feature_of_interest_name}, {self.sensors}"
