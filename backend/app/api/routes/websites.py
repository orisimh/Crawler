# app/api/routes/websites.py
from fastapi import APIRouter, Depends
from app.models.schemas import WebsitesResponse
from app.services.website_service import WebsiteService

router = APIRouter()


def get_website_service() -> WebsiteService:
    """Dependency to get website service instance"""
    return WebsiteService()


@router.get("/websites", response_model=WebsitesResponse)
async def get_websites(
        website_service: WebsiteService = Depends(get_website_service)
):
    """
    Get list of supported websites

    Returns information about all supported websites including:
    - Website name/domain
    - Base URL
    - Availability status
    """
    return website_service.get_supported_websites()