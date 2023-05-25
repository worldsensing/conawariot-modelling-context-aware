from typing import Optional, TYPE_CHECKING, List

from sqlmodel import Field, SQLModel, Relationship

from app.schemas.observation import Observation

if TYPE_CHECKING:
    from app.schemas.observable_property import ObservableProperty


class Sensor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)

    active: bool = Field(default=False)
    info: Optional[str]
    lastConnectTime: Optional[str] = Field()
    lastDisconnectTime: Optional[str] = Field()
    lastActivityTime: Optional[str] = Field()
    inactivityAlarmTime: Optional[str] = Field()

    # Relations
    # TODO Check how can it be that one of these two is Nullable
    thing_name: Optional[str] = Field(foreign_key="thing.name")
    gateway_name: Optional[str] = Field(foreign_key="gateway.name")
    observable_property_name: str = Field(nullable=False, foreign_key="observableproperty.name")
    observable_property: "ObservableProperty" = Relationship(back_populates="sensors")
    location_name: Optional[str] = Field(foreign_key="location.name")
    observations: List["Observation"] = Relationship()

    # man_id: Optional[str] = Field()
    # man_name: Optional[str] = Field()
    # man_sensor_name: Optional[str] = Field()
    # fw_version: Optional[str] = Field()
    # port: Optional[str] = Field()
    # calibration_date: Optional[str] = Field()
