from typing import Optional, TYPE_CHECKING, List

from sqlmodel import Field, SQLModel, Relationship

from app.schemas.actuation import Actuation

if TYPE_CHECKING:
    from app.schemas.actuatable_property import ActuatableProperty


class Actuator(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)

    info: Optional[str]
    lastConnectTime: Optional[str] = Field()
    lastDisconnectTime: Optional[str] = Field()
    lastActivityTime: Optional[str] = Field()
    inactivityAlarmTime: Optional[str] = Field()

    # Relations
    thing_name: str = Field(nullable=False, foreign_key="thing.name")
    actuatable_property_name: str = Field(nullable=False, foreign_key="actuatableproperty.name")
    actuatable_property: "ActuatableProperty" = Relationship(back_populates="actuators")
    response_procedure_name: Optional[str] = Field(foreign_key="responseprocedure.name")
    location_name: Optional[str] = Field(foreign_key="location.name")
    actuations: List["Actuation"] = Relationship()
    #
