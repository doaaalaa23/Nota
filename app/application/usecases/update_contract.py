from typing import Optional
from app.domain.models.contract_model import Contract
from app.domain.repositories.contract_repository import ContractRepository
from app.domain.repositories.user_repository import UserRepository


class UpdateContractUseCase:
	def __init__(self, contract_repository: ContractRepository, user_repository: UserRepository | None = None):
		self.contract_repository = contract_repository
		self.user_repository = user_repository

	def execute(self, contract_id: int,
			  contract: Contract, user_id: int | 
			  None = None) -> Optional[Contract]:

		contract.remaining_price = round(float(contract.sale_price) - float(contract.receiving_price), 2)
		contract.installment_num = int(contract.remaining_price / contract.installment_value) if contract.installment_value > 0 else 0

		if self.user_repository is not None and user_id is not None:
			user = self.user_repository.get_by_id(user_id)
			if user is None:
				raise ValueError("User not found")
			

		return self.contract_repository.update(contract_id, contract)

