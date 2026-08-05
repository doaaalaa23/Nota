from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.models.contract_model import Contract
from app.domain.repositories.contract_repository import ContractRepository
from app.infrastructure.models.client_model import ClientTable
from app.infrastructure.models.contract_model import ContractTable
from app.infrastructure.models.paying_model import PayingTable
from app.infrastructure.models.product_model import ProductTable
from app.infrastructure.models.user_model import UserTable

from sqlalchemy import func
from datetime import date
from dateutil.relativedelta import relativedelta


class ContractRepositoryImpl(ContractRepository):
    def __init__(self, session: Session, user_id: Optional[int] = None):
        self.session = session
        self.user_id = user_id

    def set_user_id(self, user_id: int) -> None:
        self.user_id = user_id

    def _require_user_id(self) -> int:
        if self.user_id is None:
            raise ValueError("User context is required")
        return self.user_id

    def _ensure_related_entities(self, contract: Contract) -> None:
        self._require_user_id()
        client = self.session.query(ClientTable).filter(
            ClientTable.client_id == contract.client_id,
            ClientTable.user_id == self.user_id,
        ).first()
        if client is None:
            raise ValueError("Client not found for current user")

        product = self.session.query(ProductTable).filter(
            ProductTable.product_id == contract.product_id,
            ProductTable.user_id == self.user_id,
        ).first()
        if product is None:
            raise ValueError("Product not found for current user")
        return product

    def _get_user_locked(self) -> UserTable:
        user_id = self._require_user_id()
       
        user = (
            self.session.query(UserTable)
            .filter(UserTable.user_id == user_id)
            .with_for_update()
            .first()
        )
        if user is None:
            raise ValueError("User not found")
        return user
    
    def create(self, contract: Contract) -> Contract:
        try:
            self._ensure_related_entities(contract)
            user = self._get_user_locked()
            product = self._ensure_related_entities(contract)

            cost = round(float(product.product_price) - float(contract.receiving_price), 2)

            if cost > float(user.balance):
                raise ValueError("Your balance is not enough to create this contract. Please add balance first.")
            table = ContractTable(
                product_id=contract.product_id,
                client_id=contract.client_id,
                user_id=self.user_id,
                sale_date=contract.sale_date,
                sale_price=contract.sale_price,
                receiving_price=contract.receiving_price,
                remaining_price=contract.remaining_price,
                installment_value=contract.installment_value,
                installment_num=contract.installment_num,
                paying_day=contract.paying_day,
                first_installment=contract.first_installment,
            )
            self.session.add(table)
            user.balance = float(user.balance) - cost
            self.session.commit()
            self.session.refresh(table)
            return Contract(
                product_id=table.product_id,
                client_id=table.client_id,
                sale_date=table.sale_date,
                sale_price=table.sale_price,
                receiving_price=table.receiving_price,
                installment_value=table.installment_value,
                paying_day=table.paying_day,
                first_installment=table.first_installment,
                contract_id=table.contract_id,
            )
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error creating contract: {str(e)}")

    def read(self, contract_id: str) -> Optional[Contract]:
        try:
            self._require_user_id()
            table = self.session.query(ContractTable).filter(
                ContractTable.contract_id == int(contract_id),
                ContractTable.user_id == self.user_id,
            ).first()
            if not table:
                return None

            return Contract(
                product_id=table.product_id,
                client_id=table.client_id,
                sale_date=table.sale_date,
                sale_price=table.sale_price,
                receiving_price=table.receiving_price,
                installment_value=table.installment_value,
                paying_day=table.paying_day,
                first_installment=table.first_installment,
                contract_id=table.contract_id,
            )
        except Exception as e:
            raise ValueError(f"Error reading contract: {str(e)}")

    def read_all(self) -> List[Contract]:
        try:
            self._require_user_id()
            tables = self.session.query(ContractTable).filter(ContractTable.user_id == self.user_id).all()
            return [
                Contract(
                    product_id=t.product_id,
                    client_id=t.client_id,
                    sale_date=t.sale_date,
                    sale_price=t.sale_price,
                    receiving_price=t.receiving_price,
                    installment_value=t.installment_value,
                    paying_day=t.paying_day,
                    first_installment=t.first_installment,
                    contract_id=t.contract_id,
                )
                for t in tables
            ]
        except Exception as e:
            raise ValueError(f"Error reading all contracts: {str(e)}")

    def update(self, contract_id: str, contract: Contract) -> Optional[Contract]:
        try:
            self._require_user_id()
            table = self.session.query(ContractTable).filter(
                ContractTable.contract_id == int(contract_id),
                ContractTable.user_id == self.user_id,
            ).first()
            if not table:
                return None
            
            product = self._ensure_related_entities(contract)
            self._ensure_related_entities(contract)

            old_cost = round(float(product.product_price) - float(table.receiving_price), 2)
            new_cost = round(float(product.product_price) - float(contract.receiving_price), 2)

            user = self._get_user_locked()

            available = float(user.balance) + old_cost

            if new_cost > available:
                raise ValueError(
                    "Your balance is not enough to update this contract. Please add balance first."
                )

            user.balance = available - new_cost
            table.product_id = contract.product_id
            table.client_id = contract.client_id
            table.sale_date = contract.sale_date
            table.sale_price = contract.sale_price
            table.receiving_price = contract.receiving_price
            table.remaining_price = contract.remaining_price
            table.installment_value = contract.installment_value
            table.installment_num = contract.installment_num
            table.paying_day = contract.paying_day
            table.first_installment = contract.first_installment

            self.session.commit()

            return Contract(
                product_id=table.product_id,
                client_id=table.client_id,
                sale_date=table.sale_date,
                sale_price=table.sale_price,
                receiving_price=table.receiving_price,
                installment_value=table.installment_value,
                paying_day=table.paying_day,
                first_installment=table.first_installment,
                contract_id=table.contract_id,
            )
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error updating contract: {str(e)}")

    def delete(self, contract_id: str) -> bool:
        try:
            self._require_user_id()
            table = self.session.query(ContractTable).filter(
                ContractTable.contract_id == int(contract_id),
                ContractTable.user_id == self.user_id,
            ).first()
            if not table:
                return False
            
            self.session.delete(table)
            self.session.commit()
            return True
        except ValueError:
            self.session.rollback()
            raise  
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error deleting contract: {str(e)}")

    def exists(self, contract_id: str) -> bool:
        try:
            self._require_user_id()
            result = self.session.query(ContractTable).filter(
                ContractTable.contract_id == int(contract_id),
                ContractTable.user_id == self.user_id,
            ).first()
            return result is not None
        except Exception as e:
            raise ValueError(f"Error checking contract existence: {str(e)}")

    def get_contract_status(self, contract_id: int) -> str:
        self._require_user_id()
        contract = (
            self.session.query(ContractTable)
            .filter(ContractTable.contract_id == contract_id, ContractTable.user_id == self.user_id)
            .first()
        )

        if contract is None:
            raise ValueError("Contract not found")

        total_paid = (
            self.session.query(func.coalesce(func.sum(PayingTable.paid_amount), 0))
            .filter(PayingTable.contract_id == contract_id, PayingTable.user_id == self.user_id)
            .scalar()
        )
        total_paid = float(total_paid)

        if total_paid >= contract.remaining_price:
            return "Completed"

        today = date.today()
        due_installments = 0

        for i in range(contract.installment_num):
            due_date = contract.first_installment + relativedelta(months=i)
            if due_date <= today:
                due_installments += 1

        expected_paid = due_installments * float(contract.installment_value)

        if total_paid < expected_paid:
            return "Late"

        return "On Time"

    def get_contract_payment_info(self, contract_id: int) -> dict:
        self._require_user_id()
        contract = (
            self.session.query(ContractTable)
            .filter(ContractTable.contract_id == contract_id, ContractTable.user_id == self.user_id)
            .first()
        )
        if contract is None:
            raise ValueError("Contract not found")

        total_paid = (
            self.session.query(func.coalesce(func.sum(PayingTable.paid_amount), 0))
            .filter(PayingTable.contract_id == contract_id, PayingTable.user_id == self.user_id)
            .scalar()
        )
        total_paid = float(total_paid)

        remaining_price = float(contract.remaining_price - total_paid)

        if total_paid >= contract.remaining_price:
            return {
                "status": "Completed",
                "total_paid": total_paid,
                "remaining_price": remaining_price,
                "delay_amount": 0.0,
            }

        today = date.today()
        due_installments = 0
        for i in range(contract.installment_num):
            due_date = contract.first_installment + relativedelta(months=i)
            if due_date <= today:
                due_installments += 1

        expected_paid = due_installments * float(contract.installment_value)
        delay_amount = max(expected_paid - total_paid, 0.0)
        status = "Late" if delay_amount > 0 else "On Time"

        return {
            "status": status,
            "total_paid": total_paid,
            "remaining_price": remaining_price,
            "delay_amount": delay_amount,
        }