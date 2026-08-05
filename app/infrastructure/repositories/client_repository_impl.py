from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.models.client_model import Client, Phone
from app.domain.repositories.client_repository import ClientRepository
from app.infrastructure.models.client_model import ClientTable, PhoneTable
from app.infrastructure.models.contract_model import ContractTable
from app.infrastructure.models.product_model import ProductTable
from app.infrastructure.models.paying_model import PayingTable
from app.infrastructure.repositories.contract_repository_impl import ContractRepositoryImpl
import traceback


class ClientRepositoryImpl(ClientRepository):
    """
    Concrete implementation of ClientRepository using SQLAlchemy ORM.
    """

    def __init__(self, session: Session, user_id: Optional[int] = None):
        """
        Initialize the repository with a database session.

        Args:
            session: SQLAlchemy session for database operations
            user_id: currently authenticated user id
        """
        self.session = session
        self.user_id = user_id
        self.contract_repository = ContractRepositoryImpl(session, user_id)

    def set_user_id(self, user_id: int) -> None:
        self.user_id = user_id
        self.contract_repository.set_user_id(user_id)

    def _require_user_id(self) -> int:
        if self.user_id is None:
            raise ValueError("User context is required")
        return self.user_id

    def create(self, client: Client) -> Client:
        try:
            self._require_user_id()
            client_table = ClientTable(
                client_id=client.client_id,
                client_name=client.client_name,
                client_email=client.client_email,
                surety=client.surety,
                surety_num=client.surety_num,
                address=client.address,
                user_id=self.user_id,
            )

            for phone in client.phone_numbers:
                phone_table = PhoneTable(number=phone.number, client_id=client.client_id)
                client_table.phone_numbers.append(phone_table)

            self.session.add(client_table)
            self.session.commit()

            return client
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error creating client: {str(e)}")

    def read(self, client_id: str) -> Optional[Client]:
        try:
            self._require_user_id()
            client_table = self.session.query(ClientTable).filter(
                ClientTable.client_id == client_id,
                ClientTable.user_id == self.user_id,
            ).first()

            if not client_table:
                return None

            return self._map_table_to_domain(client_table)
        except Exception as e:
            raise ValueError(f"Error reading client: {str(e)}")

    def read_by_name(self, client_name: str) -> List[Client]:
        try:
            self._require_user_id()
            client_table = self.session.query(ClientTable).filter(
                ClientTable.client_name.ilike(f"%{client_name}%"),
                ClientTable.user_id == self.user_id,
            ).all()

            if not client_table:
                return []

            return [self._map_table_to_domain(c) for c in client_table]
        except Exception as e:
            raise ValueError(f"Error reading client: {str(e)}")

    def read_all(self) -> List[Client]:
        try:
            self._require_user_id()
            client_tables = self.session.query(ClientTable).filter(ClientTable.user_id == self.user_id).all()
            if not client_tables:
                return []
            return [self._map_table_to_domain(ct) for ct in client_tables]
        except Exception as e:
            print("=" * 50)
            print("REPOSITORY read_all ERROR:", repr(e))
            traceback.print_exc()
            print("=" * 50)
            raise ValueError(f"Error reading all clients: {str(e)}")

    def update(self, client_id: str, client: Client) -> Optional[Client]:
        try:
            self._require_user_id()
            client_table = self.session.query(ClientTable).filter(
                ClientTable.client_id == client_id,
                ClientTable.user_id == self.user_id,
            ).first()

            if not client_table:
                return None

            client_table.client_name = client.client_name
            client_table.client_email = client.client_email
            client_table.surety = client.surety
            client_table.surety_num = client.surety_num
            client_table.address = client.address

            self.session.query(PhoneTable).filter(PhoneTable.client_id == client_id).delete()

            for phone in client.phone_numbers:
                phone_table = PhoneTable(number=phone.number, client_id=client_id)
                client_table.phone_numbers.append(phone_table)

            self.session.commit()

            return self._map_table_to_domain(client_table)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error updating client: {str(e)}")

    def delete(self, client_id: str) -> bool:
        try:
            self._require_user_id()
            client_table = self.session.query(ClientTable).filter(
                ClientTable.client_id == client_id,
                ClientTable.user_id == self.user_id,
            ).first()

            if not client_table:
                return False

            self.session.delete(client_table)
            self.session.commit()

            return True
        except Exception as e:
            self.session.rollback()
            traceback.print_exc()
            raise ValueError(f"Error deleting client: {str(e)}")

    def exists(self, client_id: str) -> bool:
        try:
            self._require_user_id()
            result = self.session.query(ClientTable).filter(
                ClientTable.client_id == client_id,
                ClientTable.user_id == self.user_id,
            ).first()

            return result is not None
        except Exception as e:
            raise ValueError(f"Error checking client existence: {str(e)}")

    def _map_table_to_domain(self, client_table: ClientTable) -> Client:
        phone_objects = [Phone(phone_table.number) for phone_table in client_table.phone_numbers]

        return Client(
            client_id=client_table.client_id,
            client_name=client_table.client_name,
            client_email=client_table.client_email,
            phone_numbers=phone_objects,
            surety=client_table.surety,
            surety_num=client_table.surety_num,
            address=client_table.address,
        )

    def account_statement(self, client_id: str) -> List[dict]:
        self._require_user_id()
        client = (
            self.session.query(ClientTable)
            .filter(ClientTable.client_id == client_id, ClientTable.user_id == self.user_id)
            .first()
        )
        if client is None:
            raise ValueError("Client not found")

        contracts = (
            self.session.query(ContractTable)
            .filter(ContractTable.client_id == client_id, ContractTable.user_id == self.user_id)
            .all()
        )

        statement = []
        for contract in contracts:
            product = (
                self.session.query(ProductTable)
                .filter(ProductTable.product_id == contract.product_id, ProductTable.user_id == self.user_id)
                .first()
            )
            payments = (
                self.session.query(PayingTable)
                .filter(PayingTable.contract_id == contract.contract_id, PayingTable.user_id == self.user_id)
                .order_by(PayingTable.paying_date.asc())
                .all()
            )

            payment_info = self.contract_repository.get_contract_payment_info(contract.contract_id)

            statement.append({
                "contract_id": contract.contract_id,
                "product_id": contract.product_id,
                "product_name": product.product_name if product else "Unknown product",
                "sale_date": contract.sale_date,
                "sale_price": float(contract.sale_price),
                "receiving_price": float(contract.receiving_price),
                "remaining_price": payment_info["remaining_price"],
                "total_paid": payment_info["total_paid"],
                "delay_amount": payment_info["delay_amount"],
                "installment_value": float(contract.installment_value),
                "installment_num": contract.installment_num,
                "installment_amount": float(contract.remaining_price), 
                "paying_day": contract.paying_day,
                "first_installment": contract.first_installment,
                "status": payment_info["status"],
                "payments": [
                    {
                        "paying_id": p.paying_id,
                        "paid_amount": float(p.paid_amount),
                        "paying_date": p.paying_date,
                        "notice": p.notice,
                    }
                    for p in payments
                ],
            })

        return statement