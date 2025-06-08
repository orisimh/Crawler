# app/models/schemas.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional



class LoginRequest(BaseModel):
    """Login request model"""
    website: str
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "website": "fo1.altius.finance",
                "username": "fo1_test_user@whatever.com",
                "password": "Test123!"
            }
        }


class LoginResponse(BaseModel):
    """Login response model"""
    success: bool
    token: Optional[str] = None
    deals: List[str] = []
    message: str

    # class Config:
    #     json_schema_extra = {
    #         "example": {
    #             "success": True,
    #             "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    #             "deals": ["Deal 1", "Deal 2", "Deal 3"],
    #             "message": "Login successful"
    #         }
    #     }


class WebsiteInfo(BaseModel):
    """Website information model"""
    name: str
    base_url: str
    available: bool = True


class WebsitesResponse(BaseModel):
    """Websites list response model"""
    websites: List[WebsiteInfo]
    count: int


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    status_code: int

class CrawlerResponse(BaseModel):
    """Login response model"""
    success: bool
    deals: List[str] = []
    message: str
