from datetime import date
from typing import List

from app.domain.models.notification_model import UserNotification
from app.domain.repositories.notification_repository import NotificationRepository


class NotifyUserUseCase:
	def __init__(self, notification_repository: NotificationRepository):
		self.notification_repository = notification_repository

	def execute(self, today: date | None = None) -> List[UserNotification]:
		return self.notification_repository.read_due_today(today or date.today())
