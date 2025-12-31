from typing import Dict, List, Optional, Tuple
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.image import Image
from app.schemas.image import ImageCreate, ImageUpdate

class ImageService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_image(self, image_data: dict) -> Image:
        db_image = Image(**image_data)
        self.db.add(db_image)
        await self.db.commit()
        await self.db.refresh(db_image)
        return db_image

    async def get_image(self, image_id: UUID) -> Optional[Image]:
        result = await self.db.execute(select(Image).filter(Image.id == image_id))
        return result.scalars().first()
        
    async def get_image_by_key(self, file_key: str) -> Optional[Image]:
        """Get an image by its file key (uploadthing_key in the database)."""
        result = await self.db.execute(
            select(Image).filter(Image.uploadthing_key == file_key)
        )
        return result.scalars().first()

    async def get_images(self, skip: int = 0, limit: int = 20) -> List[Image]:
        result = await self.db.execute(
            select(Image)
            .order_by(Image.upload_date.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
        
    async def get_images_grouped_by_year_month(self) -> Dict[str, Dict]:
        """
        Retrieve all images grouped by year and month in the format:
        {
            "year": {
                "2024": {
                    "april": { "images": [...] },
                    "june": { "images": [...] }
                },
                "2025": {
                    "april": { "images": [...] },
                    "june": { "images": [...] }
                }
            }
        }
        """
        from datetime import datetime
        from collections import defaultdict
        
        # Get all images ordered by upload date (newest first)
        result = await self.db.execute(
            select(Image)
            .order_by(Image.upload_date.desc())
        )
        images = result.scalars().all()
        
        # Group images by year and month
        grouped = defaultdict(lambda: defaultdict(dict))
        month_names = [
            'january', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december'
        ]
        
        for image in images:
            year = str(image.upload_date.year)
            month_num = image.upload_date.month
            month_name = month_names[month_num - 1].lower()
            
            # Convert SQLAlchemy model to dict to make it JSON serializable
            image_dict = {
                "id": str(image.id),
                "description": image.description,
                "upload_date": image.upload_date.isoformat(),
                "image_url": image.image_url,
                "uploadthing_key": image.uploadthing_key,
                "file_size": image.file_size,
                "mime_type": image.mime_type,
                "width": image.width,
                "height": image.height,
                "created_at": image.created_at.isoformat(),
                "updated_at": image.updated_at.isoformat() if image.updated_at else None
            }
            
            if month_name not in grouped[year]:
                grouped[year][month_name] = {"images": []}
                
            # Add the image if it's not already in the list
            if not any(img["id"] == str(image.id) for img in grouped[year][month_name]["images"]):
                grouped[year][month_name]["images"].append(image_dict)
        
        # Convert defaultdict to regular dict for JSON serialization
        return {"year": {year: dict(months) for year, months in grouped.items()}}

    async def update_image(self, image_id: UUID, image_in: ImageUpdate) -> Optional[Image]:
        db_image = await self.get_image(image_id)
        if not db_image:
            return None
        
        update_data = image_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_image, field, value)
            
        await self.db.commit()
        await self.db.refresh(db_image)
        return db_image

    async def delete_image(self, image_id: UUID) -> Optional[str]:
        """
        Deletes image from DB and returns the uploadthing_key for external deletion.
        """
        db_image = await self.get_image(image_id)
        if not db_image:
            return None
            
        key = db_image.uploadthing_key
        await self.db.delete(db_image)
        await self.db.commit()
        return key
