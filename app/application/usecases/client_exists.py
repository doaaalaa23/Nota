from app.domain.repositories.client_repository import ClientRepository


class ClientExistsUseCase:
    """
    Use case for checking whether a client exists by ID.
    """

    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository

    def execute(self, client_id: str) -> bool:
        """
        Execute the client exists use case.

        """
        return self.client_repository.exists(client_id)
