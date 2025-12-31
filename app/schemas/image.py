from datetime import datetime
from typing import Dict, List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, RootModel

class ImageBase(BaseModel):
    description: str

class ImageCreate(ImageBase):
    pass

class ImageUpdate(BaseModel):
    description: Optional[str] = None

class ImageInDBBase(ImageBase):
    id: UUID
    upload_date: datetime
    image_url: str
    uploadthing_key: str
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class Image(ImageInDBBase):
    pass

class MonthImages(BaseModel):
    images: List[Image] = Field(..., description="List of images for this month")

class YearData(RootModel):
    root: Dict[str, MonthImages] = Field(..., description="Months with their images")

class GroupedImagesResponse(BaseModel):
    year: Dict[str, Dict[str, MonthImages]] = Field(..., description="Images grouped by year and month")
