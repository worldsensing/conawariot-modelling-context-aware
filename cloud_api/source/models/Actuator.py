# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from database import Base


class Actuator(Base):
    __tablename__ = "actuator"
    id = Column(Integer, primary_key=True, nullable=False)
    thing_name = Column(String(32), ForeignKey("thing.name"))
    name = Column(String(32), unique=True, nullable=False)
    actuatable_property_name = Column(String(32),
                                      ForeignKey("actuatable_property.name", ondelete="SET NULL"))
    location_name = Column(String(32), ForeignKey('location.name', ondelete="SET NULL"))

    actuations = relationship("ActuatorActuation", back_populates="actuator")

    def __str__(self):
        return f"{self.id}, {self.thing_name}, {self.name}, {self.actuatable_property_name}" \
               f", {self.location_name}, {self.actuations}"
