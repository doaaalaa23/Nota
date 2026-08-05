from app.domain.models.product_model import Product
from app.domain.repositories.product_repository import ProductRepository


class AddProductUseCase:
    """
    Use case for adding a new product to the system.
    """

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(
        self,
        product_name: str,
        product_price: float
    ) -> Product:
        
        product = Product(
            product_name=product_name,
            product_price=product_price
        )

        return self.product_repository.add(product)
