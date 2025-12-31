import uuid
from sqlalchemy import Column, String, Text, Date, Time, DateTime, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    day = Column(String, nullable=False, index=True)
    time = Column(String, nullable=False)
    location = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
