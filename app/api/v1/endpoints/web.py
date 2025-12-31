from fastapi import APIRouter, Request, Form, UploadFile, File, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import List, Optional
import os
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.event_service import EventService
from app.schemas.event import EventCreate

router = APIRouter()

# Set up templates directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("/events/new", response_class=HTMLResponse)
async def create_event_form(request: Request):
    """Render the event creation form"""
    return templates.TemplateResponse("event_creator.html", {"request": request})

@router.post("/events")
async def create_event(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    day: str = Form(...),
    time: str = Form(...),
    location: str = Form(...),
    images: List[UploadFile] = File([]),
    db: AsyncSession = Depends(get_db)
):
    """Handle event creation with file uploads"""
    try:
        # Combine day and time into a datetime object
        event_datetime = datetime.strptime(f"{day} {time}", "%Y-%m-%d %H:%M")
        
        # Create event data
        event_data = EventCreate(
            name=name,
            description=description,
            event_datetime=event_datetime,
            location=location
        )
        
        # Save the event to the database
        event_service = EventService(db)
        event = await event_service.create_event(event_data)
        
        # Process uploaded images if any
        image_urls = []
        if images:
            # Here you would typically upload images to your storage service
            # and save the URLs to the database
            for image in images:
                # Example: Save image to disk (replace with your storage service)
                upload_dir = BASE_DIR / "static" / "uploads"
                upload_dir.mkdir(exist_ok=True)
                
                file_path = upload_dir / image.filename
                with open(file_path, "wb") as buffer:
                    content = await image.read()
                    buffer.write(content)
                
                image_url = f"/static/uploads/{image.filename}"
                image_urls.append(image_url)
        
        # Return success response
        return {
            "status": "success",
            "message": "Event created successfully",
            "event_id": str(event.id),
            "image_urls": image_urls
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )