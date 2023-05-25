import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Field, SQLModel


class Actuation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    time_start: datetime.datetime = Field(sa_column=Column(DateTime(timezone=True),
                                                           nullable=False))
    time_end: Optional[datetime.datetime] = Field(sa_column=Column(DateTime(timezone=True)))

    # Relations
    # context_aware_rule_name: str = Field(nullable=False, foreign_key="context_aware_rule.name")
    actuator_name: str = Field(nullable=False, foreign_key="actuator.name")
    actuatable_property_name: str = Field(nullable=False, foreign_key="actuatableproperty.name")
    # observation_id: Optional[int] = Field(foreign_key="observation.id")  # TODO Many-to-Many
    #
