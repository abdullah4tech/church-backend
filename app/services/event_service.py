from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate

class EventService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_event(self, event_in: EventCreate) -> Event:
        db_event = Event(**event_in.model_dump())
        self.db.add(db_event)
        await self.db.commit()
        await self.db.refresh(db_event)
        return db_event

    async def get_event(self, event_id: UUID) -> Optional[Event]:
        result = await self.db.execute(select(Event).filter(Event.id == event_id))
        return result.scalars().first()

    async def get_events(self, skip: int = 0, limit: int = 20) -> List[Event]:
        result = await self.db.execute(select(Event).offset(skip).limit(limit))
        return result.scalars().all()

    async def update_event(self, event_id: UUID, event_in: EventUpdate) -> Optional[Event]:
        db_event = await self.get_event(event_id)
        if not db_event:
            return None
        
        update_data = event_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_event, field, value)
            
        await self.db.commit()
        await self.db.refresh(db_event)
        return db_event

    async def delete_event(self, event_id: UUID) -> bool:
        db_event = await self.get_event(event_id)
        if not db_event:
            return False
            
        await self.db.delete(db_event)
        await self.db.commit()
        return True
