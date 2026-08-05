from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.models.paying_model import Paying
from app.domain.repositories.paying_repository import PayingRepository
from app.infrastructure.models.client_model import ClientTable
from app.infrastructure.models.contract_model import ContractTable
from app.infrastructure.models.paying_model import PayingTable
from app.infrastructure.models.user_model import UserTable


class PayingRepositoryImpl(PayingRepository):
    def __init__(self, session: Session, user_id: Optional[int] = None):
        self.session = session
        self.user_id = user_id

    def set_user_id(self, user_id: int) -> None:
        self.user_id = user_id

    def _require_user_id(self) -> int:
        if self.user_id is None:
            raise ValueError("User context is required")
        return self.user_id

    def _ensure_contract_belongs_to_user(self, contract_id: int, client_id: str) -> None:
        self._require_user_id()
        contract = self.session.query(ContractTable).filter(
            ContractTable.contract_id == contract_id,
            ContractTable.user_id == self.user_id,
        ).first()
        if contract is None:
            raise ValueError("Contract not found for current user")

        client = self.session.query(ClientTable).filter(
            ClientTable.client_id == client_id,
            ClientTable.user_id == self.user_id,
        ).first()
        if client is None:
            raise ValueError("Client not found for current user")

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

    def create(self, paying: Paying) -> Paying:
        try:
            self._ensure_contract_belongs_to_user(paying.contract_id, paying.client_id)
            user = self._get_user_locked()

            table = PayingTable(
                paid_amount=paying.paid_amount,
                contract_id=paying.contract_id,
                client_id=paying.client_id,
                user_id=self.user_id,
                paying_date=paying.paying_date,
                notice=paying.notice,
            )
            self.session.add(table)
            user.balance = float(user.balance) + float(paying.paid_amount)

            self.session.commit()
            self.session.refresh(table)
            return Paying(
                paid_amount=table.paid_amount,
                contract_id=table.contract_id,
                client_id=table.client_id,
                paying_date=table.paying_date,
                notice=table.notice,
                paying_id=table.paying_id,
            )
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error creating paying: {str(e)}")

    def update(self, paying: Paying) -> Paying:
        try:
            self._require_user_id()
            table = self.session.query(PayingTable).filter(
                PayingTable.paying_id == int(paying.paying_id),
                PayingTable.user_id == self.user_id,
            ).first()
            if not table:
                raise ValueError(f"Paying with ID {paying.paying_id} not found")
            
            old_paid_amount = float(table.paid_amount)
            user = self._get_user_locked()

            self._ensure_contract_belongs_to_user(paying.contract_id, paying.client_id)
            table.paid_amount = paying.paid_amount
            table.contract_id = paying.contract_id
            table.client_id = paying.client_id
            table.paying_date = paying.paying_date
            table.notice = paying.notice



            user.balance = float(user.balance) - float(old_paid_amount)+ float(paying.paid_amount)

            self.session.commit()
            self.session.refresh(table)
            return Paying(
                paid_amount=table.paid_amount,
                contract_id=table.contract_id,
                client_id=table.client_id,
                paying_date=table.paying_date,
                notice=table.notice,
                paying_id=table.paying_id,
            )
        except ValueError:
            raise
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error updating paying: {str(e)}")

    def read(self, paying_id: int) -> Optional[Paying]:
        try:
            self._require_user_id()
            table = self.session.query(PayingTable).filter(
                PayingTable.paying_id == int(paying_id),
                PayingTable.user_id == self.user_id,
            ).first()
            if not table:
                return None
            return Paying(
                paid_amount=table.paid_amount,
                contract_id=table.contract_id,
                client_id=table.client_id,
                paying_date=table.paying_date,
                notice=table.notice,
                paying_id=table.paying_id,
            )
        except Exception as e:
            raise ValueError(f"Error reading paying: {str(e)}")

    def read_all(self) -> List[Paying]:
        try:
            self._require_user_id()
            tables = self.session.query(PayingTable).filter(PayingTable.user_id == self.user_id).all()
            return [
                Paying(
                    paid_amount=t.paid_amount,
                    contract_id=t.contract_id,
                    client_id=t.client_id,
                    paying_date=t.paying_date,
                    notice=t.notice,
                    paying_id=t.paying_id,
                )
                for t in tables
            ]
        except Exception as e:
            raise ValueError(f"Error reading all payings: {str(e)}")

    def read_by_contract(self, contract_id: int) -> List[Paying]:
        try:
            self._require_user_id()
            tables = self.session.query(PayingTable).filter(
                PayingTable.contract_id == int(contract_id),
                PayingTable.user_id == self.user_id,
            ).all()
            return [
                Paying(
                    paid_amount=t.paid_amount,
                    contract_id=t.contract_id,
                    client_id=t.client_id,
                    paying_date=t.paying_date,
                    notice=t.notice,
                    paying_id=t.paying_id,
                )
                for t in tables
            ]
        except Exception as e:
            raise ValueError(f"Error reading payings for contract: {str(e)}")

    def delete(self, paying_id: int) -> bool:
        try:
            self._require_user_id()
            user = self._get_user_locked()

            table = self.session.query(PayingTable).filter(
                PayingTable.paying_id == int(paying_id),
                PayingTable.user_id == self.user_id,
            ).first()
            if not table:
                return False
            self.session.delete(table)
            user.balance = float(user.balance) - float(table.paid_amount)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error deleting paying: {str(e)}")

    def exists(self, paying_id: int) -> bool:
        try:
            self._require_user_id()
            table = self.session.query(PayingTable).filter(
                PayingTable.paying_id == int(paying_id),
                PayingTable.user_id == self.user_id,
            ).first()
            return table is not None
        except Exception as e:
            raise ValueError(f"Error checking paying existence: {str(e)}")