# backend_core/api/v1/api.py
from fastapi import APIRouter

from backend_core.api.v1.endpoints import auth, users

api_router = APIRouter()

# Add routers from endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
