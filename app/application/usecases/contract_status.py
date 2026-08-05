from app.domain.repositories.contract_repository import ContractRepository

class GetContractStatusUseCase:

    def __init__(self, contract_repo: ContractRepository):
        self.contract_repo = contract_repo

    def execute(self, contract_id: int) -> str:
        return self.contract_repo.get_contract_status(contract_id)