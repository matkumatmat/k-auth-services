from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.config.server.Settings import settings

def setup_cors(app):
    """Configure CORS middleware for the FastAPI application."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )