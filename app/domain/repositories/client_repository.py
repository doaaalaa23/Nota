from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.client_model import Client


class ClientRepository(ABC):
    """
    Abstract repository class for Client CRUD operations.
    """

    @abstractmethod
    def set_user_id(self, user_id: int) -> None:
        """Bind subsequent operations to the authenticated user."""
        pass
    
    @abstractmethod
    def create(self, client: Client) -> Client:
        """
        Create a new client record.
        
        Args:
            client: Client object to be created
            
        Returns:
            Created Client object
        """
        pass
    
    @abstractmethod
    def read(self, client_id: str) -> Optional[Client]:
        """
        Read a client by ID.
        
        Args:
            client_id: The ID of the client to retrieve
            
        Returns:
            Client object if found, None otherwise
        """
        pass
    @abstractmethod
    def read_by_name(self, client_name: str) -> List[Client]:
        """
        Read clients by name.
        
        Args:
            client_name: The name filter to search
            
        Returns:
            List of Client domain objects
        """
        pass
    @abstractmethod
    def read_all(self) -> List[Client]:
        """
        Read all clients.
        
        Returns:
            List of all Client objects
        """
        pass
    
    @abstractmethod
    def update(self, client_id: str, client: Client) -> Optional[Client]:
        """
        Update an existing client record.
        
        Args:
            client_id: The ID of the client to update
            client: Updated Client object
            
        Returns:
            Updated Client object if successful, None otherwise
        """
        pass
    
    @abstractmethod
    def delete(self, client_id: str) -> bool:
        """
        Delete a client record.
        
        Args:
            client_id: The ID of the client to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def exists(self, client_id: str) -> bool:
        """
        Check if a client exists.
        
        Args:
            client_id: The ID of the client to check
            
        Returns:
            True if client exists, False otherwise
        """
        pass
    @abstractmethod
    def account_statement(self, client_id: str) -> List[dict]:
        """
        Retrieve the full account statement for a client:
        every contract the client holds, each enriched with its
        product name, computed status (On Time / Late), and full
        payment history.

        Returns a list of dicts, one per contract, shaped like:
        {
            "contract_id": int,
            "product_id": int,
            "product_name": str,
            "sale_date": date,
            "sale_price": float,
            "receiving_price": float,
            "remaining_price": float,
            "installment_value": float,
            "installment_num": int,
            "paying_day": int,
            "first_installment": date,
            "installment_amount": float,
            "status": str,              # "On Time" | "Late"
            "payments": [
                {
                    "paying_id": int,
                    "paid_amount": float,
                    "paying_date": date,
                    "notice": str | None,
                },
                ...
            ],
        }
        """
        pass