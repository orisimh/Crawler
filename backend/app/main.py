# main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api.routes import auth, websites
from fastapi.responses import JSONResponse
from app.services.auth.jwt_handler import decode_access_token
from app.services.auth.dependencies import extract_final_path
from typing import List, Optional
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Site Crawler API", version="1.0.0")
settings = get_settings()


# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.allowed_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def check_token_middleware(request: Request, call_next):

    if request.url.path.startswith("/docs") : # or request.url.path.startswith("/login")
        return await call_next(request)

    token = request.headers.get("token")
    route_endpoint = extract_final_path(request)
    if  route_endpoint not in ["login"] and (not token or not decode_access_token(token) ): #
        return JSONResponse(status_code=401, content={"detail":"Unauthorized or token expired"})

    return await call_next(request)

# Routers
app.include_router(auth.router, prefix=f"/api/{settings.v}", tags=["authentication"])
app.include_router(websites.router, prefix=f"/api/{settings.v}", tags=["websites"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.host, port=settings.port) # , reload=True

