from typing import List
from app.domain.models.product_model import Product
from app.domain.repositories.product_repository import ProductRepository


class GetAllProductUseCase:
    """
    Use case for retrieving all products.
    """

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self) -> List[Product]:
        return self.product_repository.read_all()
