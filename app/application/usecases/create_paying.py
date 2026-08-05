from datetime import date
from app.domain.models.paying_model import Paying
from app.domain.repositories.paying_repository import PayingRepository
from app.domain.repositories.user_repository import UserRepository


class CreatePayingUseCase:
    def __init__(self, paying_repository: PayingRepository, user_repository: UserRepository | None = None):
        self.paying_repository = paying_repository
        self.user_repository = user_repository

    def execute(
        self,
        paid_amount: float,
        contract_id: int,
        client_id: str,
        paying_date: date,
        notice: str,
        user_id: int | None = None,
    ) -> Paying:
        paying = Paying(
            paid_amount=paid_amount,
            contract_id=contract_id,
            client_id=client_id,
            paying_date=paying_date,
            notice=notice,
        )
        created = self.paying_repository.create(paying)

        if self.user_repository is not None and user_id is not None:
            user = self.user_repository.get_by_id(user_id)
            if user is None:
                raise ValueError("User not found")

        return created
