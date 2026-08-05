from datetime import date
from typing import Optional
import math


class Contract:
    """
    Contract model representing an installment agreement between a client and the business.
    """

    def __init__(
        self,
        product_id: int,
        client_id: str,
        sale_date: date,
        sale_price: float,
        receiving_price: float,
        installment_value: float,
        paying_day: int,
        first_installment: date,
        contract_id: Optional[int] = None,
    ):
        # ID may be None for new contracts (database autoincrement)
        self.contract_id = contract_id
        self.product_id = product_id
        self.client_id = client_id
        self.sale_date = sale_date
        self.sale_price = sale_price
        self.receiving_price = receiving_price

        # Derived values
        self.remaining_price = round(float(sale_price) - float(receiving_price), 2)
        # Use ceiling to ensure full coverage if not exact division
        self.installment_value = installment_value
        self.installment_num = int(math.ceil(float(self.remaining_price) / float(installment_value))) if installment_value > 0 else 0

        self.paying_day = paying_day
        self.first_installment = first_installment

    def __repr__(self):
        return (
            f"Contract(id={self.contract_id}, product_id={self.product_id}, "
            f"client_id={self.client_id}, sale_price={self.sale_price}, "
            f"installment_value={self.installment_value}, "
            f"installment_num={self.installment_num})"
        )
