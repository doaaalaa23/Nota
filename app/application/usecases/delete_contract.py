from app.domain.repositories.contract_repository import ContractRepository


class DeleteContractUseCase:
	def __init__(self, contract_repository: ContractRepository):
		self.contract_repository = contract_repository

	def execute(self, contract_id: int) -> bool:
		return self.contract_repository.delete(contract_id)

