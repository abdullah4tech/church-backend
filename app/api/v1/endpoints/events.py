from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.event import Event, EventCreate, EventUpdate
from app.services.event_service import EventService

router = APIRouter()

@router.post("/", response_model=Event, status_code=status.HTTP_201_CREATED)
async def create_event(
    event_in: EventCreate,
    db: AsyncSession = Depends(get_db)
):
    service = EventService(db)
    return await service.create_event(event_in)

@router.get("/", response_model=List[Event])
async def read_events(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    service = EventService(db)
    return await service.get_events(skip=skip, limit=limit)

@router.get("/{event_id}", response_model=Event)
async def read_event(
    event_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    service = EventService(db)
    event = await service.get_event(event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event

@router.put("/{event_id}", response_model=Event)
async def update_event(
    event_id: UUID,
    event_in: EventUpdate,
    db: AsyncSession = Depends(get_db)
):
    service = EventService(db)
    event = await service.update_event(event_id, event_in)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    service = EventService(db)
    success = await service.delete_event(event_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
