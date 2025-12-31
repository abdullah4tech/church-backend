from typing import Dict, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.image import Image, ImageUpdate, GroupedImagesResponse
from app.services.image_db_service import ImageService
from app.services.image_service import ImageProcessor
from app.services.storage_service import StorageService

router = APIRouter()

@router.post("/", response_model=Image, status_code=status.HTTP_201_CREATED)
async def upload_image(
    file: UploadFile = File(...),
    description: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    # 1. Process Image
    try:
        content = await file.read()
        processed_file, width, height, fmt = ImageProcessor.process_image(content)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # 2. Upload to B2
    storage_service = StorageService()
    try:
        # We need to pass the processed file content. 
        # Since StorageService expects a file-like object,
        # we pass the BytesIO object.
        filename = f"{file.filename.split('.')[0]}.{fmt.lower()}"
        # StorageService is synchronous (boto3)
        upload_res = storage_service.upload_file(processed_file, filename)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to upload image: {str(e)}")

    # 3. Save Metadata to DB
    image_data = {
        "description": description,
        "image_url": upload_res["url"],
        "uploadthing_key": upload_res["key"], # We keep the column name for now, but it stores B2 key
        "file_size": processed_file.getbuffer().nbytes,
        "mime_type": f"image/{fmt.lower()}",
        "width": width,
        "height": height
    }
    
    db_service = ImageService(db)
    return await db_service.create_image(image_data)

@router.get("/", response_model=List[Image])
async def read_images(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a paginated list of all images, ordered by upload date (newest first)
    """
    service = ImageService(db)
    return await service.get_images(skip=skip, limit=limit)

@router.get("/grouped", response_model=GroupedImagesResponse)
async def read_images_grouped(
    db: AsyncSession = Depends(get_db)
):
    """
    Get all images grouped by year and month
    """
    service = ImageService(db)
    result = await service.get_images_grouped_by_year_month()
    return result

@router.get("/{image_id}", response_model=Image)
async def read_image(
    image_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    service = ImageService(db)
    image = await service.get_image(image_id)
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return image

@router.put("/{image_id}", response_model=Image)
async def update_image(
    image_id: UUID,
    image_in: ImageUpdate,
    db: AsyncSession = Depends(get_db)
):
    service = ImageService(db)
    image = await service.update_image(image_id, image_in)
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return image

@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(
    image_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    service = ImageService(db)
    # Get key before deleting from DB
    image = await service.get_image(image_id)
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    
    key = image.uploadthing_key
    
    # Delete from DB
    await service.delete_image(image_id)
    
    # Delete from B2
    storage_service = StorageService()
    storage_service.delete_file(key)

@router.get("/serve/{file_key}", response_class=Response)
async def serve_image(
    file_key: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Serve an image by its file key.
    This endpoint acts as a proxy to serve images from Backblaze B2.
    """
    # Verify the image exists in our database
    image_service = ImageService(db)
    image = await image_service.get_image_by_key(file_key)
    
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    # Get the image from B2
    storage_service = StorageService()
    try:
        file_content, content_type = storage_service.download_file(file_key)
        
        # Return the image data with appropriate headers
        return Response(
            content=file_content,
            media_type=content_type,
            headers={"Cache-Control": "public, max-age=31536000"}  # Cache for 1 year
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve image: {str(e)}"
        )
