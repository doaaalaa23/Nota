from typing import Optional
from app.domain.models.contract_model import Contract
from app.domain.repositories.contract_repository import ContractRepository


class GetContractUseCase:
	def __init__(self, contract_repository: ContractRepository):
		self.contract_repository = contract_repository

	def execute(self, contract_id: int) -> Optional[Contract]:
		return self.contract_repository.read(contract_id)

