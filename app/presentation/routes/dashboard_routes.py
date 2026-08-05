from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.presentation.schemas.dashboard_schema import DashboardStatsResponse
from app.application.usecases.get_dashboard_stats import GetDashboardStatsUseCase
from app.domain.repositories.dashboard_repository import DashboardRepository
from app.infrastructure.repositories.dashboard_repository_impl import DashboardRepositoryImpl
from app.infrastructure.database.session import get_db
from app.presentation.routes.dependencies import get_current_user_id
import traceback

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


def get_dashboard_repository(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> DashboardRepository:
    repository = DashboardRepositoryImpl(db)
    repository.set_user_id(user_id)
    return repository


def get_dashboard_stats_use_case(
    repository: DashboardRepository = Depends(get_dashboard_repository),
) -> GetDashboardStatsUseCase:
    return GetDashboardStatsUseCase(repository)


@router.get("/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats(
    use_case: GetDashboardStatsUseCase = Depends(get_dashboard_stats_use_case),
):
    try:
        return use_case.execute()
    except Exception as e:
        traceback.print_exc() 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))