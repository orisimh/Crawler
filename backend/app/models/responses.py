from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class LoginResponse(BaseModel):
    """Response model for login operations"""
    success: bool = Field(..., description="Whether the login was successful")
    token: Optional[str] = Field(None, description="Authentication token if available")
    deals: List[str] = Field(default=[], description="List of available deals/items")
    message: str = Field(..., description="Response message")
    error: Optional[str] = Field(None, description="Error message if login failed")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "deals": ["Deal 1: Special Offer", "Deal 2: Premium Package"],
                "message": "Successfully logged into fo1.altius.finance",
                "error": None,
                "timestamp": "2024-01-15T10:30:00"
            }
        }

class WebsiteListResponse(BaseModel):
    """Response model for supported websites list"""
    websites: List[str] = Field(..., description="List of supported websites")
    count: int = Field(..., description="Number of supported websites")

    def __init__(self, websites: List[str], **data):
        super().__init__(websites=websites, count=len(websites), **data)

    class Config:
        schema_extra = {
            "example": {
                "websites": ["fo1.altius.finance", "fo2.altius.finance"],
                "count": 2
            }
        }

class ValidationResult(BaseModel):
    """Response model for validation operations"""
    is_valid: bool = Field(..., description="Whether the validation passed")
    message: str = Field(..., description="Validation message")
    error_message: Optional[str] = Field(None, description="Error details if validation failed")

class WebsiteStatus(BaseModel):
    """Response model for website status check"""
    is_accessible: bool = Field(..., description="Whether the website is accessible")
    response_time: Optional[float] = Field(None, description="Response time in seconds")
    status_code: Optional[int] = Field(None, description="HTTP status code")
    message: str = Field(..., description="Status message")
    checked_at: datetime = Field(default_factory=datetime.now, description="When the check was performed")

class TestCredentials(BaseModel):
    """Response model for test credentials"""
    username: str = Field(..., description="Test username")
    password: str = Field(..., description="Test password")

    class Config:
        schema_extra = {
            "example": {
                "username": "fo1_test_user@whatever.com",
                "password": "Test123!"
            }
        }