from typing import List
from app.domain.models.paying_model import Paying
from app.domain.repositories.paying_repository import PayingRepository


class GetPayingsByContractUseCase:
    def __init__(self, paying_repository: PayingRepository):
        self.paying_repository = paying_repository

    def execute(self, contract_id: int) -> List[Paying]:
        return self.paying_repository.read_by_contract(contract_id)
