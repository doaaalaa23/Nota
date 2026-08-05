from typing import List, Optional
from app.domain.models.client_model import Client, Phone
from app.domain.repositories.client_repository import ClientRepository


class CreateClientUseCase:
    """
    Use case for creating a new client in the system.
    """
    
    def __init__(self, client_repository: ClientRepository):
        """
        Initialize the CreateClientUseCase with a ClientRepository dependency.
        
        Args:
            client_repository: Repository instance for client operations
        """
        self.client_repository = client_repository
    
    def execute(
        self,
        client_id: str,
        client_name: str,
        client_email: Optional[str],
        phone_numbers: List[str],
        surety: str,
        surety_num: str,
        address: str
    ) -> Client:
        """
        Execute the create client use case.
        
        Args:
            client_id: Unique identifier for the client
            client_name: Full name of the client
            phone_numbers: List of client's phone numbers
            surety: Surety information
            surety_num: Surety number
            address: Client's address
            
        Returns:
            The created Client object
            
        Raises:
            ValueError: If client already exists or validation fails
        """
        # Validate that client doesn't already exist
        if self.client_repository.exists(client_id):
            raise ValueError(f"Client with ID {client_id} already exists")
        
        
        # Convert phone numbers to Phone objects
        phone_objects = [Phone(number) for number in phone_numbers]
        
        # Create new client instance
        client = Client(
            client_id=client_id,
            client_name=client_name,
            client_email=client_email,
            phone_numbers=phone_objects,
            surety=surety,
            surety_num=surety_num,
            address=address
        )
        
        # Save to repository
        created_client = self.client_repository.create(client)
        
        return created_client
    
   