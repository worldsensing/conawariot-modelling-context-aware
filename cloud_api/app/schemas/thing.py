from typing import Optional, List

from sqlmodel import Field, SQLModel, Relationship

from app.schemas.actuator import Actuator
from app.schemas.sensor import Sensor


class Thing(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)

    active: bool = Field(default=False)
    info: Optional[str]
    sampling_rate: Optional[str] = Field()
    lastConnectTime: Optional[str] = Field()
    lastDisconnectTime: Optional[str] = Field()
    lastActivityTime: Optional[str] = Field()
    inactivityAlarmTime: Optional[str] = Field()

    # Relations
    # TODO List Relation instead of FKs
    group_name: Optional[str] = Field(foreign_key="group.name")
    # TODO List Relation instead of FKs
    gateway_name: Optional[str] = Field(foreign_key="gateway.name")
    sensors: List["Sensor"] = Relationship()
    actuators: List["Actuator"] = Relationship()
    location_name: Optional[str] = Field(foreign_key="location.name")
    #
