# backend_core/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend_core.api.v1.api import api_router
from backend_core.core.config import settings
from backend_core.db.utils import check_database_connection

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "Welcome to the API", "version": settings.VERSION, "docs_url": "/docs"}


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    db_status = "healthy" if check_database_connection() else "unhealthy"
    return {"status": "ok", "database": db_status, "version": settings.VERSION}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler."""
    return JSONResponse(status_code=500, content={"detail": "Internal server error", "path": request.url.path})
