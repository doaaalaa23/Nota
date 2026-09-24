from datetime import date
from typing import List, Optional

from dateutil.relativedelta import relativedelta
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.domain.models.notification_model import UserNotification
from app.domain.repositories.notification_repository import NotificationRepository
from app.infrastructure.models.client_model import ClientTable
from app.infrastructure.models.contract_model import ContractTable
from app.infrastructure.models.paying_model import PayingTable


class NotificationRepositoryImpl(NotificationRepository):
	def __init__(self, session: Session, user_id: Optional[int] = None):
		self.session = session
		self.user_id = user_id

	def set_user_id(self, user_id: int) -> None:
		self.user_id = user_id

	def _require_user_id(self) -> int:
		if self.user_id is None:
			raise ValueError("User context is required")
		return self.user_id

	def read_due_today(self, today: date) -> List[UserNotification]:
		user_id = self._require_user_id()
		contracts = (
			self.session.query(ContractTable, ClientTable.client_name)
			.join(ClientTable, ClientTable.client_id == ContractTable.client_id)
			.filter(
				ContractTable.user_id == user_id,
				ClientTable.user_id == user_id,
			)
			.all()
		)

		paid_by_contract = dict(
			self.session.query(
				PayingTable.contract_id,
				func.coalesce(func.sum(PayingTable.paid_amount), 0),
			)
			.filter(PayingTable.user_id == user_id)
			.group_by(PayingTable.contract_id)
			.all()
		)

		notifications: List[UserNotification] = []
		for contract, client_name in contracts:
			installment_value = float(contract.installment_value or 0)
			if installment_value <= 0:
				continue

			paid_installments = int(
				float(paid_by_contract.get(contract.contract_id, 0) or 0)
				// installment_value
			)
			for installment_index in range(contract.installment_num):
				due_date = contract.first_installment + relativedelta(months=installment_index)
				if due_date != today or installment_index < paid_installments:
					continue

				notifications.append(
					UserNotification(
						contract_id=contract.contract_id,
						client_id=contract.client_id,
						client_name=client_name,
						installment_number=installment_index + 1,
						installment_amount=installment_value,
						due_date=due_date,
					)
				)
				break

		return notifications
