from typing import List
from app.domain.models.paying_model import Paying
from app.domain.repositories.paying_repository import PayingRepository


class GetAllPayingsUseCase:
    def __init__(self, paying_repository: PayingRepository):
        self.paying_repository = paying_repository

    def execute(self) -> List[Paying]:
        return self.paying_repository.read_all()
