from app.domain.models.client_model import Client, Phone
from app.domain.repositories.client_repository import ClientRepository


class UpdateClientUseCase:
    """
    Use case for updating an existing client.
    """

    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository

    def execute(self, client_id: str, client: Client) -> Client:
        if not self.client_repository.exists(client_id):
            raise ValueError(f"Client with ID {client_id} not found")

        updated_client = self.client_repository.update(client_id, client)

        if updated_client is None:
            raise ValueError(f"Could not update client with ID {client_id}")

        return updated_client