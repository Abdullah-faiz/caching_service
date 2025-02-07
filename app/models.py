import uuid

from sqlmodel import SQLModel, Field

from typing import Optional


class String(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    original: str = Field(unique=True, index=True)
    transformed: str

class Payload(SQLModel, table=True):

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    output: str
    