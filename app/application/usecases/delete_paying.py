from app.domain.repositories.paying_repository import PayingRepository


class DeletePayingUseCase:
    def __init__(self, paying_repository: PayingRepository):
        self.paying_repository = paying_repository

    def execute(self, paying_id: int) -> bool:
        return self.paying_repository.delete(paying_id)
