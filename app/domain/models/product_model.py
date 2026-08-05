from typing import Optional


class Product:
    """
    Product model representing items available for purchase on installment.
    """
    
    def __init__(
        self,
        product_name: str,
        product_price: float,
        product_id: Optional[int] = None
    ):
        self.product_id = product_id
        self.product_name = product_name
        self.product_price = product_price
    
    def __repr__(self):
        return (
            f"Product(id={self.product_id}, name='{self.product_name}', "
            f"price={self.product_price})"
        )
