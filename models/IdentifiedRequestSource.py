from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class IdentifiedRequestSource(SQLModel, table=True):
    __tablename__ = "request_source"
    id: Optional[int] = Field(default=None, primary_key=True)
    ip: str = Field(unique=True)

    captured_requests: List["CapturedRequest"] = Relationship(back_populates="request_source")
