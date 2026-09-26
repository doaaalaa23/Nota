from datetime import date
 
 
class UserNotification:
    def __init__(
        self,
        contract_id: int,
        client_id: str,
        client_name: str,
        installment_number: int,
        installment_amount: float,
        due_date: date,
    ):
        self.contract_id = contract_id
        self.client_id = client_id
        self.client_name = client_name
        self.installment_number = installment_number
        self.installment_amount = installment_amount
        self.due_date = due_date