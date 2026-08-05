from datetime import date
from typing import Optional


class Paying:
    """
    Paying model representing payment records for installment contracts.
    """
    
    def __init__(
        self,
        paid_amount: float,
        contract_id: int,
        client_id: str,
        paying_date: date,
        notice: str,
        paying_id: Optional[int] = None,
    ):
        self.paying_id = paying_id
        self.paid_amount = paid_amount
        self.contract_id = contract_id
        self.client_id = client_id
        self.paying_date = paying_date
        self.notice = notice
    def __repr__(self):
        return (
            f"Paying(id={self.paying_id}, amount={self.paid_amount}, contract_id={self.contract_id}, "
            f"client_id={self.client_id}, date={self.paying_date}, "
            f"notice='{self.notice}')"
        )
