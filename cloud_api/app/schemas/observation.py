import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Field, SQLModel


class Observation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    time_start: datetime.datetime = Field(sa_column=Column(DateTime(timezone=True),
                                                           nullable=False))

    time_end: Optional[datetime.datetime] = Field(sa_column=Column(DateTime(timezone=True)))

    # TODO Improve handling of the value system
    value_int: Optional[int]
    value_float: Optional[float]
    value_bool: Optional[bool]
    value_str: Optional[str]

    # Relations
    observable_property_name: str = Field(nullable=False, foreign_key="observableproperty.name")
    sensor_name: str = Field(nullable=False, foreign_key="sensor.name")
    # actuation_id: Optional[int] = Field(foreign_key="actuation.id")  # TODO Many-to-Many
    #
