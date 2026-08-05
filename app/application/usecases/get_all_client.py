from typing import List
from app.domain.models.client_model import Client
from app.domain.repositories.client_repository import ClientRepository


class GetAllClientUseCase:
    """
    Use case for retrieving all Clients .
    """

    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository

    def execute(self) -> List[Client]:
        clients = self.client_repository.read_all()
        if not clients:
          print("No clients found")
        return clients
