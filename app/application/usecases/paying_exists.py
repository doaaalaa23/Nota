from app.domain.repositories.paying_repository import PayingRepository


class PayingExistsUseCase:
    def __init__(self, paying_repository: PayingRepository):
        self.paying_repository = paying_repository

    def execute(self, paying_id: int) -> bool:
        return self.paying_repository.exists(paying_id)
