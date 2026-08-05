from datetime import date

from app.domain.models.paying_model import Paying
from app.domain.repositories.paying_repository import PayingRepository


class UpdatePayingUseCase:
    """
    Use case for updating an existing Paying.
    """

    def __init__(self, paying_repository: PayingRepository):
        self.paying_repository = paying_repository

    def execute(
        self,
        paying_id: int,
        paid_amount: float,
        paying_date: date,
        notice: str,
    ) -> Paying:
        existing_paying = self.paying_repository.read(paying_id)
        if existing_paying is None:
            raise ValueError(f"Paying with ID {paying_id} not found")

        updated_paying = Paying(
            paying_id=paying_id,
            paid_amount=paid_amount,
            contract_id=existing_paying.contract_id,
            client_id=existing_paying.client_id,
            paying_date=paying_date,
            notice=notice,
        )

        result = self.paying_repository.update(updated_paying)

        if result is None:
            raise ValueError(f"Could not update paying with ID {paying_id}")

        return result