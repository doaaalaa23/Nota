from dataclasses import dataclass
from app.domain.repositories.user_repository import UserRepository

@dataclass
class GetUserBalanceUseCase:
    user_repository: UserRepository

    def execute(self, user_id: int):
        return self.user_repository.get_balance(user_id)