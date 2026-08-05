from abc import ABC, abstractmethod
from app.domain.models.dashboard_model import DashboardStats


class DashboardRepository(ABC):

    @abstractmethod
    def set_user_id(self, user_id: int) -> None:
        """Bind subsequent operations to the authenticated user."""
        pass

    @abstractmethod
    def get_dashboard_stats(self) -> DashboardStats:
        """Compute and return aggregate ledger statistics."""
        pass