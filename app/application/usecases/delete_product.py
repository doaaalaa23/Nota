from app.domain.repositories.product_repository import ProductRepository


class DeleteProductUseCase:
    """
    Use case for deleting a product from the system.
    """

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, product_id: int) -> bool:
        if not self.product_repository.exists(str(product_id)):
            raise ValueError(f"Product with ID {product_id} not found")

        deleted = self.product_repository.delete(str(product_id))
        if not deleted:
            raise ValueError(f"Could not delete product with ID {product_id}")

        return deleted
