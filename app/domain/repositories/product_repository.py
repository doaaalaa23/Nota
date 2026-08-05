from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.product_model import Product

class ProductRepository(ABC):
    """
    Abstract repository class for Product CRUD operations.
    """

    @abstractmethod
    def set_user_id(self, user_id: int) -> None:
        """Bind subsequent operations to the authenticated user."""
        pass
    
    @abstractmethod
    def add(self, product: Product) -> Product:
        """
        Create a new product record.
        
        Args:
            product: Product object to be created
            
        Returns:
            Created Product object
        """
        pass
    
    @abstractmethod
    def read(self, product_id: str) -> Optional[Product]:
        """
        Read a product by ID.
        
        Args:
            product_id: The ID of the product to retrieve
            
        Returns:
            Product object if found, None otherwise
        """
        pass

    @abstractmethod
    def read_by_name(self, product_name: str) ->List[Product]:
            """
            Read a product by name.
            
            Args:
                product_name: The name of the product to retrieve
                
            Returns:
                Product object if found, None otherwise
            """
            pass
    
    @abstractmethod
    def read_all(self) -> List[Product]:
        """
        Read all products.
        
        Returns:
            List of all Product objects
        """
        pass
    
    @abstractmethod
    def update(self, product_id: str, product: Product) -> Optional[Product]:
        """
        Update an existing product record.
        
        Args:
            product_id: The ID of the product to update
            product: Updated Product object
            
        Returns:
            Updated Product object if successful, None otherwise
        """
        pass
    
    @abstractmethod
    def delete(self, product_id: str) -> bool:
        """
        Delete a product record.
        
        Args:
            product_id: The ID of the product to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def exists(self, product_id: str) -> bool:
        """
        Check if a product exists.
        
        Args:
            product_id: The ID of the product to check
            
        Returns:
            True if product exists, False otherwise
        """
        pass
