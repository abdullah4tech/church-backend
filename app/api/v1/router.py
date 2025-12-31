from fastapi import APIRouter

from app.api.v1.endpoints import events, images, contact, web

api_router = APIRouter()
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(images.router, prefix="/images", tags=["images"])
api_router.include_router(contact.router, prefix="/contact", tags=["contact"])
api_router.include_router(web.router, tags=["web"])
