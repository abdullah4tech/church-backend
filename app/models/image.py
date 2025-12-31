import uuid
from sqlalchemy import Column, String, Text, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(Text, nullable=False)
    upload_date = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    image_url = Column(String, nullable=False)
    uploadthing_key = Column(String, nullable=False, unique=True)
    file_size = Column(Integer)
    mime_type = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
