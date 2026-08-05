from app.domain.repositories.contract_repository import ContractRepository

class ContractExistsUseCase:
	def __init__(self, contract_repository: ContractRepository):
		self.contract_repository = contract_repository

	def execute(self, contract_id: int) -> bool:
		return self.contract_repository.exists(contract_id)

