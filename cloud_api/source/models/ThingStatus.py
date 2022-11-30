from sqlalchemy import Column, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database import Base


class ThingStatus(Base):
    __tablename__ = 'thing_status'
    thing_name = Column(ForeignKey('thing.name'), primary_key=True)
    platform_name = Column(ForeignKey('platform.name'), primary_key=True)
    status = Column(Boolean, default=True)

    thing = relationship("Thing", back_populates="platforms")
    platform = relationship("Platform", back_populates="things")

    def __str__(self):
        return f"{self.thing_name}, {self.platform_name}, {self.status}"
