from app.domain.repositories.client_repository import ClientRepository


class DeleteClientUseCase:
    """
    Use case for deleting a client from the system.
    """

    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository

    def execute(self, client_id: str) -> bool:
        if not self.client_repository.exists(client_id):
            raise ValueError(f"Client with ID {client_id} not found")

        return self.client_repository.delete(client_id)
