from pydantic import BaseModel, EmailStr
from typing import List, Optional


class PhoneSchema(BaseModel):
    """
    Schema for Phone data.
    """
    number: str


class CreateClientRequest(BaseModel):
    """
    Schema for creating a new client.
    """
    client_id: str
    client_name: str
    client_email: Optional[EmailStr] = None
    phone_numbers: List[str]
    surety: str
    surety_num: str
    address: str


class ClientResponse(BaseModel):
    """
    Schema for client response data.
    """
    client_id: str
    client_name: str
    client_email: Optional[str] = None
    phone_numbers: List[PhoneSchema]
    surety: str
    surety_num: str
    address: str
    
    class Config:
        from_attributes = True


class UpdateClientRequest(BaseModel):
    """
    Schema for updating an existing client.
    Note: client_id is taken from URL path, not the request body
    """
    client_name: str
    client_email: Optional[EmailStr] = None
    phone_numbers: List[str]
    surety: str
    surety_num: str
    address: str
