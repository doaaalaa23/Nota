from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.application.usecases.notifi_user import NotifyUserUseCase
from app.domain.repositories.notification_repository import NotificationRepository
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.notifi_user_impl import NotificationRepositoryImpl
from app.presentation.routes.dependencies import get_current_user_id
from app.presentation.schemas.notification_schema import NotificationResponse


router = APIRouter(prefix="/api/notifications", tags=["notifications"])


def get_notification_repository(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> NotificationRepository:
    repository = NotificationRepositoryImpl(db)
    repository.set_user_id(user_id)
    return repository


@router.get("/today", response_model=List[NotificationResponse])
def get_today_notifications(
    repository: NotificationRepository = Depends(get_notification_repository),
):
    try:
        return NotifyUserUseCase(repository).execute()
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc