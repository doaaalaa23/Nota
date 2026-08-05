from app.domain.models.client_model import Client
from app.domain.repositories.client_repository import ClientRepository
from typing import List

class GetClientUseCase:
    """Use case for retrieving a single client by ID."""

    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository

    def execute(self, client_id: str) -> Client:
        client = self.client_repository.read(str(client_id))
        if not client:
            raise ValueError(f"Client with ID {client_id} not found")
        return client


class GetClientByNameUseCase:
    """Use case for retrieving clients by name."""

    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository

    def execute(self, client_name: str) -> List[Client]:
            return self.client_repository.read_by_name(client_name)
    