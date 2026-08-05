from app.domain.models.product_model import Product
from app.domain.repositories.product_repository import ProductRepository


class UpdateProductUseCase:
    """
    Use case for updating an existing product.
    """

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(
        self,
        product_id: int,
        product_name: str,
        product_price: float
    ) -> Product:
        if not self.product_repository.exists(str(product_id)):
            raise ValueError(f"Product with ID {product_id} not found")

        product = Product(
            product_id=product_id,
            product_name=product_name,
            product_price=product_price
        )

        updated_product = self.product_repository.update(
            str(product_id),
            product
        )

        if updated_product is None:
            raise ValueError(f"Could not update product with ID {product_id}")

        return updated_product
