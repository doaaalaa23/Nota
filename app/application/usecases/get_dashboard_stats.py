from app.domain.repositories.dashboard_repository import DashboardRepository
from app.domain.models.dashboard_model import DashboardStats


class GetDashboardStatsUseCase:

    def __init__(self, dashboard_repo: DashboardRepository):
        self.dashboard_repo = dashboard_repo

    def execute(self) -> DashboardStats:
        return self.dashboard_repo.get_dashboard_stats()