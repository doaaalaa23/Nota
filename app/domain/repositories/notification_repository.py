from abc import ABC, abstractmethod
from datetime import date
from typing import List

from app.domain.models.notification_model import UserNotification


class NotificationRepository(ABC):
    @abstractmethod
    def set_user_id(self, user_id: int) -> None:
        pass

    @abstractmethod
    def read_due_today(self, today: date) -> List[UserNotification]:
        pass
