from datetime import date

from pydantic import BaseModel


class NotificationResponse(BaseModel):
    contract_id: int
    client_id: str
    client_name: str
    installment_number: int
    installment_amount: float
    due_date: date

    class Config:
        from_attributes = True