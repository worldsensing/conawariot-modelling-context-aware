# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class FeatureOfInterest(Base):
    __tablename__ = "feature_of_interest"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(32), unique=True, nullable=False)
    location_name = Column(String(32), ForeignKey('location.name', ondelete="SET NULL"))
    observable_properties = relationship('ObservableProperty')
    actuatable_properties = relationship('ActuatableProperty')

    # Add enums?

    def __str__(self):
        return f"{self.id}, {self.name}, {self.location_name}, {self.observable_properties}, " \
               f"{self.actuatable_properties}"
