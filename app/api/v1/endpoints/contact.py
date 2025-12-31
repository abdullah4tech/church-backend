from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.contact import ContactForm
from app.services.email_service import EmailService

router = APIRouter()

@router.post("/contact", status_code=status.HTTP_200_OK)
async def send_contact_email(
    contact_data: ContactForm,
    db: AsyncSession = Depends(get_db)
):
    """
    Handle contact form submission and send an email.
    """
    email_service = EmailService()
    
    try:
        success = await email_service.send_contact_email(
            name=contact_data.name,
            email=contact_data.email,
            message=contact_data.message
        )
        
        if success:
            return {"message": "Your message has been sent successfully!"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send email. Please try again later."
            )
            
    except Exception as e:
        print(f"Error in contact endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request."
        )
