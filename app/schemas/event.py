from datetime import date, time, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class EventBase(BaseModel):
    name: str
    description: str
    day: str
    time: str
    location: str

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    day: Optional[str] = None
    time: Optional[str] = None
    location: Optional[str] = None

class EventInDBBase(EventBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class Event(EventInDBBase):
    pass
