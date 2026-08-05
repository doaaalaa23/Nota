from typing import List
from app.domain.models.contract_model import Contract
from app.domain.repositories.contract_repository import ContractRepository


class GetAllContractUseCase:
	def __init__(self, contract_repository: ContractRepository):
		self.contract_repository = contract_repository

	def execute(self) -> List[Contract]:
		return self.contract_repository.read_all()

