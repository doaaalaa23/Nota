from dataclasses import dataclass
from app.domain.repositories.user_repository import UserRepository

@dataclass
class SetUserBalanceUseCase:
    user_repository: UserRepository

    def execute(self, user_id: int, balance: float):
        return self.user_repository.update_balance(user_id, balance)