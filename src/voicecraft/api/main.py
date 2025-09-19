"""
FastAPI application for VoiceCraft API server
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import uvicorn

from .routers import create_mcp_app
from .middleware import setup_middleware
from .dependencies import get_logger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title="VoiceCraft API",
        description="AI-powered speech synthesis API with MCP support",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    # Setup middleware
    setup_middleware(app)
    
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "message": "VoiceCraft API Server",
            "version": "0.1.0",
            "docs": "/docs",
            "endpoints": {
                "mcp": "/api/v1/mcp"
            }
        }
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {"status": "healthy", "service": "voicecraft-api"}
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        """Global exception handler"""
        logger = get_logger()
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "detail": str(exc)}
        )
    
    mcp = create_mcp_app(app)
    mcp_app = mcp.http_app()
    app = FastAPI(title="VoiceCraft API", lifespan=mcp_app.lifespan)

    # Include routers
    app.mount("/api/v1", mcp_app)

    return app

# Create app instance
app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "voicecraft.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
