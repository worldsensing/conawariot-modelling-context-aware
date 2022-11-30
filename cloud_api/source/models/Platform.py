# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Platform(Base):
    __tablename__ = "platform"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(32), unique=True, nullable=False)
    location_name = Column(String(32), ForeignKey('location.name', ondelete="SET NULL"))

    things = relationship("ThingStatus", back_populates="platform")

    # TODO Add reflexive relation to other Platforms?

    def __str__(self):
        return f"{self.id}, {self.name}, {self.location_name}, {self.things}"
