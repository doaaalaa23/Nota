from pydantic import BaseModel
from datetime import date


class CreateContractRequest(BaseModel):
    product_id: int
    client_id: str
    sale_date: date
    sale_price: float
    receiving_price: float
    installment_value: float
    paying_day: int
    first_installment: date


class UpdateContractRequest(BaseModel):
    product_id: int
    sale_date: date
    sale_price: float
    receiving_price: float
    installment_value: float
    paying_day: int
    first_installment: date


class ContractResponse(BaseModel):
    contract_id: int
    product_id: int
    client_id: str
    sale_date: date
    sale_price: float
    receiving_price: float
    remaining_price: float
    installment_value: float
    installment_num: int
    paying_day: int
    first_installment: date

    class Config:
        from_attributes = True
