from app.models.schemas import CrawlerResponse
# from app.core.browser import BrowserManager
# from app.core.config import WEBSITE_CONFIGS
import logging
import time
# import aiohttp
import asyncio


import logging
from typing import Dict, List
from app.core.config import get_settings
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


logger = logging.getLogger(__name__)


class CrawlerService:
    """Service to log in via browser automation and extract deals"""

    def __init__(self):
        self.settings = get_settings()

    async def login_and_fetch_deals(self, website: str, username: str, password: str) -> Dict:
        if website not in self.settings.websites:
            return CrawlerResponse(
                success = False,
                deals = [],
                message = f"Unsupported website: {website}"
            )

        website_config = self.settings.websites[website]
        base_url = website_config["base_url"]

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(base_url, timeout=self.settings.request_timeout * 1000)

                # These selectors will vary based on the actual site!
                await page.fill('input[name="email"]', username)
                await page.fill('input[name="password"]', password)
                await page.click('button[type="submit"]')

                # Wait for navigation after login
                await page.wait_for_load_state('networkidle')

                await page.wait_for_selector(f".{self.settings.deals_name_html.replace(' ','.')}" , timeout=10000) # '.MuiStack-root.css-1s6kxhl'

                content = await page.content()
                deals = self._extract_deal_names_from_html(content)

                await browser.close()

                return CrawlerResponse(
                    success = True,
                    deals = deals,
                    message = "Login and crawl successful"
                )

        except Exception as e:
            logger.error(f"Error during crawling for {website}: {e}")
            return CrawlerResponse(
                success = False,
                deals = [],
                message =  f"Error during crawling: {str(e)}"
            )

    def _extract_deal_names_from_html(self, html: str) -> List[str]:

        soup = BeautifulSoup(html, "html.parser")
        deal_names = []

        # Find all top-level deal blocks
        deal_blocks = soup.find_all("div", class_=self.settings.deals_name_html)

        for block in deal_blocks:

            child_divs = block.find_all("div", recursive=False)
            for div in child_divs:

                # Inside each deal block, find all <p> elements
                p_tags = div.find_all("p")
                for p in p_tags:
                    text = p.get_text(strip=True)

                    # Heuristic: take only the first <p> in the block (assuming it's the deal name)
                    if text and len(deal_names) == 0 or p == p_tags[0]:
                        deal_names.append(text)
                        break  # only grab the first relevant <p>

        return deal_names or ["No deals found"]

# class CrawlerService:
#     """Service for handling web crawling operations"""
#
#     def __init__(self):
#         self.browser_manager = BrowserManager()
#
#     async def perform_login(self, website: str, username: str, password: str) -> LoginResponse:
#         """
#         Perform login to specified website
#         """
#         if website not in WEBSITE_CONFIGS:
#             return LoginResponse(
#                 success=False,
#                 message="Unsupported website",
#                 error=f"Website {website} is not supported"
#             )
#
#         config = WEBSITE_CONFIGS[website]
#
#         try:
#             # Initialize browser
#             await self.browser_manager.setup()
#
#             # Navigate to login page
#             logger.info(f"Navigating to {config['login_url']}")
#             await self.browser_manager.navigate_to(config['login_url'])
#
#             # Perform login steps
#             login_success = await self._execute_login_steps(username, password, config)
#
#             if not login_success:
#                 return LoginResponse(
#                     success=False,
#                     message="Login failed",
#                     error="Could not complete login process"
#                 )
#
#             # Check for login errors
#             error_message = await self._check_for_login_errors()
#             if error_message:
#                 return LoginResponse(
#                     success=False,
#                     message="Login failed",
#                     error=error_message
#                 )
#
#             # Extract data after successful login
#             token = await self._extract_auth_token()
#             deals = await self._extract_deals(config['deals_selector'])
#
#             return LoginResponse(
#                 success=True,
#                 token=token,
#                 deals=deals,
#                 message=f"Successfully logged into {website}"
#             )
#
#         except Exception as e:
#             logger.error(f"Login failed with exception: {str(e)}")
#             return LoginResponse(
#                 success=False,
#                 message="Login failed",
#                 error=f"Unexpected error: {str(e)}"
#             )
#         finally:
#             await self.browser_manager.cleanup()
#
#     async def check_website_status(self, website: str) -> WebsiteStatus:
#         """
#         Check if a website is accessible
#         """
#         if website not in WEBSITE_CONFIGS:
#             return WebsiteStatus(
#                 is_accessible=False,
#                 message=f"Website {website} is not configured"
#             )
#
#         config = WEBSITE_CONFIGS[website]
#         url = config.get('url') or config.get('login_url')
#
#         start_time = time.time()
#
#         try:
#             timeout = aiohttp.ClientTimeout(total=30)
#             async with aiohttp.ClientSession(timeout=timeout) as session:
#                 async with session.get(url) as response:
#                     response_time = time.time() - start_time
#
#                     return WebsiteStatus(
#                         is_accessible=response.status < 400,
#                         response_time=response_time,
#                         status_code=response.status,
#                         message=f"Website responded with status {response.status}"
#                     )
#
#         except asyncio.TimeoutError:
#             return WebsiteStatus(
#                 is_accessible=False,
#                 response_time=time.time() - start_time,
#                 message="Website request timed out"
#             )
#         except Exception as e:
#             return WebsiteStatus(
#                 is_accessible=False,
#                 response_time=time.time() - start_time,
#                 message=f"Error accessing website: {str(e)}"
#             )
#
#     async def _execute_login_steps(self, username: str, password: str, config: dict) -> bool:
#         """
#         Execute the login steps on the website
#         """
#         try:
#             # Wait for page to load
#             await self.browser_manager.page.wait_for_timeout(2000)
#
#             # Fill username
#             if not await self._fill_username_field(username, config['username_selector']):
#                 return False
#
#             # Fill password
#             if not await self._fill_password_field(password, config['password_selector']):
#                 return False
#
#             # Click login button
#             if not await self._click_login_button(config['login_button_selector']):
#                 return False
#
#             # Wait for login response
#             await self._wait_for_login_response()
#
#             return True
#
#         except Exception as e:
#             logger.error(f"Error executing login steps: {str(e)}")
#             return False
#
#     async def _fill_username_field(self, username: str, selector: str) -> bool:
#         """Fill username field"""
#         return await self.browser_manager.fill_field(selector, username, "username")
#
#     async def _fill_password_field(self, password: str, selector: str) -> bool:
#         """Fill password field"""
#         return await self.browser_manager.fill_field(selector, password, "password")
#
#     async def _click_login_button(self, selector: str) -> bool:
#         """Click login button"""
#         return await self.browser_manager.click_element(selector, "login button")
#
#     async def _wait_for_login_response(self):
#         """Wait for login response"""
#         try:
#             await self.browser_manager.page.wait_for_load_state('networkidle', timeout=10000)
#         except Exception as e:
#             logger.warning(f"Navigation timeout: {str(e)}")
#
#     async def _check_for_login_errors(self) -> str:
#         """Check for login error messages"""
#         try:
#             error_selectors = [
#                 ".error", ".alert-danger", ".invalid-feedback",
#                 "[class*='error']", "[class*='invalid']",
#                 "div:has-text('Invalid')", "div:has-text('Error')",
#                 ".message.error", ".error-message"
#             ]
#
#             for selector in error_selectors:
#                 error_element = await self.browser_manager.page.query_selector(selector)
#                 if error_element:
#                     error_text = await error_element.text_content()
#                     if error_text and any(word in error_text.lower()
#                                           for word in ['invalid', 'error', 'wrong', 'incorrect', 'failed']):
#                         return f"Authentication error: {error_text.strip()}"
#
#             return None
#         except Exception as e:
#             logger.error(f"Error checking for login errors: {str(e)}")
#             return None
#
#     async def _extract_auth_token(self) -> str:
#         """Extract authentication token"""
#         return await self.browser_manager.extract_auth_token()
#
#     async def _extract_deals(self, deals_selector: str) -> list:
#         """Extract available deals"""
#         return await self.browser_manager.extract_deals(deals_selector)