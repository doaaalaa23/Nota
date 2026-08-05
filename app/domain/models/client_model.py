class Phone:
    def __init__(self, number: str):
        self.number = number
from typing import Optional

class Client:
    """
    Client model representing a customer in the installment system.
    """
    
    def __init__(
        self,
        client_id: str,
        client_name: str,
        client_email: Optional[str],
        phone_numbers:list[Phone],
        surety: str,
        surety_num: str,
        address: str
    ):
        self.client_id = client_id
        self.client_name = client_name
        self.client_email = client_email
        self.phone_numbers = phone_numbers
        self.surety = surety
        self.surety_num = surety_num
        self.address = address
    
    def __repr__(self):
        return (
            f"Client(id={self.client_id}, name='{self.client_name}', "
            f"email='{self.client_email}', phone='{', '.join(phone.number for phone in self.phone_numbers)}', surety='{self.surety_num}', "
            f"address='{self.address}')"
        )
