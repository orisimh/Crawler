from pydantic import BaseModel, Field, validator
from typing import Optional

class LoginRequest(BaseModel):
    """Request model for user login"""
    website: str = Field(..., description="Website domain to login to", min_length=1)
    username: str = Field(..., description="Username or email for login", min_length=1)
    password: str = Field(..., description="Password for login", min_length=1)

    @validator('website')
    def validate_website(cls, v):
        if not v or not v.strip():
            raise ValueError('Website cannot be empty')
        return v.strip().lower()

    @validator('username')
    def validate_username(cls, v):
        if not v or not v.strip():
            raise ValueError('Username cannot be empty')
        return v.strip()

    @validator('password')
    def validate_password(cls, v):
        if not v or not v.strip():
            raise ValueError('Password cannot be empty')
        return v

    class Config:
        schema_extra = {
            "example": {
                "website": "fo1.altius.finance",
                "username": "fo1_test_user@whatever.com",
                "password": "Test123!"
            }
        }

class WebsiteStatusRequest(BaseModel):
    """Request model for checking website status"""
    website: str = Field(..., description="Website domain to check")
    timeout: Optional[int] = Field(30, description="Timeout in seconds", ge=1, le=120)

    class Config:
        schema_extra = {
            "example": {
                "website": "fo1.altius.finance",
                "timeout": 30
            }
        }