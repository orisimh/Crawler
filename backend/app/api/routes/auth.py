# app/api/routes/auth.py
from fastapi import APIRouter, HTTPException, Depends, status
from app.models.schemas import LoginRequest, LoginResponse, CrawlerResponse
from app.services.auth.auth_service import AuthService
import logging
from app.services.crawler_service import CrawlerService

logger = logging.getLogger(__name__)

router = APIRouter()


def get_auth_service() -> AuthService:
    """Dependency to get auth service instance"""
    return AuthService()


@router.post("/login", response_model=LoginResponse)
async def login(
        request: LoginRequest,
        auth_service: AuthService = Depends(get_auth_service)
):
    """
    Login to a website with provided credentials

    - **website**: The website domain (e.g., fo1.altius.finance)
    - **username**: User's username or email
    - **password**: User's password
    """
    try:

        auth_result: LoginResponse = await auth_service.login_to_website(
            website=request.website,
            username=request.username,
            password=request.password
        )

        if( not auth_result.success):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=auth_result.message)

        crawler = CrawlerService()
        deals_result: CrawlerResponse = await crawler.login_and_fetch_deals(request.website, request.username, request.password)

        if (not deals_result.success):
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail=deals_result.message)

        return LoginResponse(  success = deals_result.success,
                                token = auth_result.token,
                                deals = deals_result.deals,
                                message =  deals_result.message
                            )

    except Exception as e:
        logger.error(f"Login endpoint error: {e}")
        status_code = getattr(e, "status_code", 500)
        detail = getattr(e, "detail", str(e) or "Internal server error")
        raise HTTPException(status_code=status_code, detail=detail)




