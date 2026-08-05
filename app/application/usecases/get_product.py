from typing import List
from app.domain.models.product_model import Product
from app.domain.repositories.product_repository import ProductRepository


class GetProductUseCase:
    """
    Use case for retrieving a single product by ID.
    """

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, product_id: int) -> Product:
        product = self.product_repository.read(str(product_id))
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")
        return product


class GetProductByNameUseCase:
    """
    Use case for retrieving a single product by name.
    """

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, product_name: str) -> List[Product]:
        return self.product_repository.read_by_name(product_name)