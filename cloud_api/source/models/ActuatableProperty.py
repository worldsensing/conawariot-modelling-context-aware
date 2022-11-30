# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class ActuatableProperty(Base):
    __tablename__ = "actuatable_property"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(32), unique=True, nullable=False)
    feature_of_interest_name = Column(String(32),
                                      ForeignKey("feature_of_interest.name", ondelete="cascade"))
    actuators = relationship("Actuator")

    # Add enums?

    def __str__(self):
        return f"{self.id}, {self.name}, {self.feature_of_interest_name}, {self.actuators}"
