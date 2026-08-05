from datetime import date
from pydantic import BaseModel


class CreatePayingRequest(BaseModel):
    paid_amount: float
    contract_id: int
    client_id: str
    paying_date: date
    notice: str


class PayingResponse(BaseModel):
    paying_id: int
    paid_amount: float
    contract_id: int
    client_id: str
    paying_date: date
    notice: str

    class Config:
        from_attributes = True


class UpdatePayingRequest(BaseModel):
    paid_amount: float
    paying_date: date
    notice: str