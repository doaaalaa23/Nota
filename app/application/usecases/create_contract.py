from datetime import date
from app.domain.models.contract_model import Contract
from app.domain.repositories.contract_repository import ContractRepository
from app.domain.repositories.user_repository import UserRepository


class CreateContractUseCase:
	"""Use case to create a new contract. Computes remaining_price and installment_num."""

	def __init__(self, contract_repository: ContractRepository, user_repository: UserRepository | None = None):
		self.contract_repository = contract_repository
		self.user_repository = user_repository

	def execute(
		self,
		product_id: int,
		client_id: str,
		sale_date: date,
		sale_price: float,
		receiving_price: float,
		installment_value: float,
		paying_day: int,
		first_installment: date,
		user_id: int | None = None,
	) -> Contract:
		contract = Contract(
			product_id=product_id,
			client_id=client_id,
			sale_date=sale_date,
			sale_price=sale_price,
			receiving_price=receiving_price,
			installment_value=installment_value,
			paying_day=paying_day,
			first_installment=first_installment,
		)

		if self.user_repository is not None and user_id is not None:
			user = self.user_repository.get_by_id(user_id)
			if user is None:
				raise ValueError("User not found")
			
		created = self.contract_repository.create(contract)
		return created

