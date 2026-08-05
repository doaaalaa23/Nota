from app.domain.repositories.product_repository import ProductRepository


class ProductExistsUseCase:
    """
    Use case for checking whether a product exists by ID.
    """

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, product_id: int) -> bool:
        """
        Execute the product exists use case.

        Args:
            product_id: The ID of the product to check.

        Returns:
            True if the product exists, False otherwise.
        """
        return self.product_repository.exists(str(product_id))
