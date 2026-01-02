from datetime import datetime, timezone
from typing import Optional, Dict, Any
from sqlmodel import Field, SQLModel, JSON, Column, Relationship

class CapturedRequest(SQLModel, table=True):
    __tablename__ = "captured_request"
    id: Optional[int] = Field(default=None, primary_key=True)
    request_time: float = datetime.now(timezone.utc).timestamp()
    headers: Dict[str, Any] = Field(sa_column=Column(JSON), default_factory=dict)

    request_source_id: Optional[int] = Field(default=None, foreign_key="request_source.id")
    request_source: Optional["IdentifiedRequestSource"] = Relationship(back_populates="captured_requests")