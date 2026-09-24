import asyncio
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
from app.presentation.routes.notification_routes import router as notification_router
from app.infrastructure.database.database import init_db
from app.infrastructure.database.session import get_session
from app.infrastructure.models.user_model import UserTable
from app.infrastructure.notifications.email_notification_service import EmailNotificationService
from app.infrastructure.repositories.notifi_user_impl import NotificationRepositoryImpl
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse

# Initialize FastAPI app
app = FastAPI(
    title="Installment System API",
    description="A comprehensive system for managing clients, products, contracts, and payments",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

notification_task: asyncio.Task | None = None


def send_due_installment_emails() -> None:
    email_service = EmailNotificationService()
    if not email_service.is_configured:
        print("Daily installment emails skipped: SMTP is not configured")
        return

    db = get_session()
    try:
        users = db.query(UserTable).filter(UserTable.is_active.is_(True)).all()
        for user in users:
            repository = NotificationRepositoryImpl(db, user.user_id)
            notifications = repository.read_due_today(__import__("datetime").date.today())
            if not notifications:
                continue
            try:
                email_service.send_due_installment_email(
                    recipient=user.email,
                    user_name=user.user_name,
                    notifications=notifications,
                )
                print(f"Sent installment email to {user.email}")
            except Exception as exc:
                print(f"Could not send installment email to {user.email}: {exc}")
    finally:
        db.close()


async def notification_loop() -> None:
    while True:
        await asyncio.to_thread(send_due_installment_emails)
        await asyncio.sleep(24 * 60 * 60)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print("VALIDATION ERROR:")
    print(exc.errors())
    print("BODY:", exc.body)
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://nota.doaaalaa237.workers.dev",
    ],
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
        global notification_task
        notification_task = asyncio.create_task(notification_loop())
    except Exception as e:
        print(f"✗ Database initialization failed: {str(e)}")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Cleanup on application shutdown.
    """
    if notification_task is not None:
        notification_task.cancel()
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
app.include_router(notification_router)


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint - serves the public landing page.
    """
    return FileResponse(static_path / "landing.html")


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
