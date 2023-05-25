import enum
from typing import Optional

from sqlmodel import Column, Enum, Field, SQLModel


class ProcedureTypeEnum(enum.Enum):
    EMAIL = "EMAIL"
    HTTP = "HTTP"


class ProcedureType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)

    procedure_type: ProcedureTypeEnum = Field(sa_column=Column(Enum(ProcedureTypeEnum)),
                                              nullable=False)
