from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.presentation.routes.client_routes import router as client_router
from app.presentation.routes.product_routes import router as product_router
from app.presentation.routes.contract_routes import router as contract_router
from app.presentation.routes.paying_routes import router as paying_router
from app.presentation.routes.dashboard_routes import router as dashboard_router
from app.presentation.routes.auth_routes import router as auth_router
from app.infrastructure.database.database import init_db
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# Initialize FastAPI app
app = FastAPI(
    title="Installment System API",
    description="A comprehensive system for managing clients, products, contracts, and payments",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print("VALIDATION ERROR:")
    print(exc.errors())
    print("BODY:", exc.body)
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """
    Initialize database tables on application startup.
    """
    try:
        init_db()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Database initialization failed: {str(e)}")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Cleanup on application shutdown.
    """
    print("✓ Application shutdown")


# Serve static files
static_path = Path(__file__).parent / "presentation" / "static"
app.mount("/static", StaticFiles(directory=static_path), name="static")


# Include routers
app.include_router(client_router)
app.include_router(product_router)
app.include_router(contract_router)
app.include_router(paying_router)
app.include_router(dashboard_router)
app.include_router(auth_router)


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint - redirects to the frontend page.
    
    Returns:
        Welcome message with link to frontend
    """
    return {
        "message": "Welcome to Installment System API",
        "version": "1.0.0",
        "status": "running",
        "frontend": "/static/index.html",
        "docs": "/docs"
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        API health status
    """
    return {
        "status": "healthy",
        "message": "API is running"
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors.
    
    Args:
        request: HTTP request
        exc: Exception
        
    Returns:
        Error response
    """
    return {
        "error": "Internal Server Error",
        "message": str(exc),
        "status_code": 500
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
