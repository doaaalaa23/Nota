from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.contract_model import Contract

class ContractRepository(ABC):
    """
    Abstract repository class for Contract CRUD operations.
    """

    @abstractmethod
    def set_user_id(self, user_id: int) -> None:
        """Bind subsequent operations to the authenticated user."""
        pass
    
    @abstractmethod
    def create(self, contract: Contract) -> Contract:
        """
        Create a new contract record.
        
        Args:
            contract: Contract object to be created
            
        Returns:
            Created Contract object
        """
        pass
    
    @abstractmethod
    def read(self, contract_id: str) -> Optional[Contract]:
        """
        Read a contract by ID.
        
        Args:
            contract_id: The ID of the contract to retrieve
            
        Returns:
            Contract object if found, None otherwise
        """
        pass
    
    @abstractmethod
    def read_all(self) -> List[Contract]:
        """
        Read all contracts.
        
        Returns:
            List of all Contract objects
        """
        pass
    
    @abstractmethod
    def update(self, contract_id: str, contract: Contract) -> Optional[Contract]:
        """
        Update an existing contract record.
        
        Args:
            contract_id: The ID of the contract to update
            contract: Updated Contract object
            
        Returns:
            Updated Contract object if successful, None otherwise
        """
        pass
    
    @abstractmethod
    def delete(self, contract_id: str) -> bool:
        """
        Delete a contract record.
        
        Args:
            contract_id: The ID of the contract to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def exists(self, contract_id: str) -> bool:
        """
        Check if a contract exists.
        
        Args:
            contract_id: The ID of the contract to check
            
        Returns:
            True if contract exists, False otherwise
        """
        pass
    @abstractmethod
    def get_contract_status(self, contract_id: int) -> str:
        """
        Get the status of a contract.
        
        Args:
            contract_id: The ID of the contract
            
        Returns:
            Status of the contract as a string
        """
        pass
    
    @abstractmethod
    def get_contract_payment_info(self, contract_id: int) -> dict:
      pass