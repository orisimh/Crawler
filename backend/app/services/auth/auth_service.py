# app/services/auth_service.py
from typing import Dict, List
import logging
from app.core.config import get_settings
from app.models.schemas import LoginResponse
from app.services.auth.jwt_handler import create_access_token

logger = logging.getLogger(__name__)


class AuthService:
    """Authentication service for handling website logins"""

    def __init__(self):
        self.settings = get_settings()

    async def login_to_website(self, website: str, username: str, password: str) -> Dict:
        """
        Attempt to login to the specified website with given credentials
        """

        if website not in self.settings.websites:
            return LoginResponse(**{
                "success": False,
                "token": None,
                "message": f"Unsupported website: {website}"
            })

        website_config = self.settings.websites[website]

        username_test = website_config["test_username"]
        password_test = website_config["test_password"]

        if ( username_test == username and password_test == password ):

            token = create_access_token({"sub": username})

            return LoginResponse(**{
                "success": True,
                "token": token,
                "message": f"Authentication successful for {website}"
            })
        else:
            return LoginResponse(**{
                "success": False,
                "token": None,
                "message": f"wrong username or password"
            })

