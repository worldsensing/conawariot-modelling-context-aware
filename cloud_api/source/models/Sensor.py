# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Sensor(Base):
    __tablename__ = "sensor"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(32), unique=True, nullable=False)
    thing_name = Column(String(32), ForeignKey("thing.name"))
    observable_property_name = Column(String(32),
                                      ForeignKey("observable_property.name", ondelete="SET NULL"))
    location_name = Column(String(32), ForeignKey('location.name', ondelete="SET NULL"))
    observations = relationship("Observation")

    def __str__(self):
        return f"{self.id}, {self.name}, {self.thing_name}, {self.observable_property_name}" \
               f", {self.location_name}, {self.observations}"
