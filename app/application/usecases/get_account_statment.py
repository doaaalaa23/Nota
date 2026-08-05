from app.domain.repositories.client_repository import ClientRepository
from typing import List


class GetAccountStatementUseCase:
    def __init__(self, client_repository: ClientRepository):
            self.client_repository = client_repository

    def execute(self, client_id: str) -> dict:
        client = self.client_repository.read(client_id)
        if client is None:
            raise ValueError("Client not found")

        contracts = self.client_repository.account_statement(client_id)

        return {
            "client": {
                "client_id": client.client_id,
                "client_name": client.client_name,
                "client_email": client.client_email,
                "phone_numbers": [p.number for p in client.phone_numbers],
                "surety": client.surety,
                "surety_num": client.surety_num,
                "address": client.address,
            },
            "summary": {
                "total_paid": sum(c["total_paid"] for c in contracts),
                "total_remaining": sum(c["remaining_price"] for c in contracts),
                "total_delayed": sum(c["delay_amount"] for c in contracts),
            },
            "contracts": contracts,
        }