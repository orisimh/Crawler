# app/services/website_service.py
from typing import List
from app.core.config import get_settings
from app.models.schemas import WebsiteInfo, WebsitesResponse


class WebsiteService:
    """Service for managing website information"""

    def __init__(self):
        self.settings = get_settings()

    def get_supported_websites(self) -> WebsitesResponse:
        """Get list of supported websites"""
        websites = []

        for website_name, config in self.settings.websites.items():
            website_info = WebsiteInfo(
                name=website_name,
                base_url=config["base_url"],
                available=True  # You could add health checks here
            )
            websites.append(website_info)

        return WebsitesResponse(
            websites=websites,
            count=len(websites)
        )

    def get_website_config(self, website_name: str) -> dict:
        """Get configuration for a specific website"""
        return self.settings.websites.get(website_name)

    def is_website_supported(self, website_name: str) -> bool:
        """Check if a website is supported"""
        return website_name in self.settings.websites