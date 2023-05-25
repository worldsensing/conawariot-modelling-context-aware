from typing import Optional

from sqlmodel import Field, SQLModel


class Group(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)

    # Relations
    # TODO Check relationship instead of FKs
    thing_name: Optional[str] = Field(foreign_key="thing.name")
    gateway_name: Optional[str] = Field(foreign_key="gateway.name")
    # TODO Add relation to other Groups
    location_name: Optional[str] = Field(foreign_key="location.name")
    #
