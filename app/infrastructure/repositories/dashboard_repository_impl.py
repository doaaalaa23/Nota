from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.domain.repositories.dashboard_repository import DashboardRepository
from app.domain.models.dashboard_model import DashboardStats

from app.infrastructure.models.contract_model import ContractTable
from app.infrastructure.models.paying_model import PayingTable
from app.infrastructure.models.client_model import ClientTable
from app.infrastructure.models.product_model import ProductTable


class DashboardRepositoryImpl(DashboardRepository):

    def __init__(self, session: Session, user_id: int | None = None):
        self.session = session
        self.user_id = user_id

    def set_user_id(self, user_id: int) -> None:
        self.user_id = user_id

    def _require_user_id(self) -> int:
        if self.user_id is None:
            raise ValueError("User context is required")
        return self.user_id

    def get_dashboard_stats(self) -> DashboardStats:
        self._require_user_id()
        total_clients = self.session.query(func.count(ClientTable.client_id)).filter(
            ClientTable.user_id == self.user_id
        ).scalar() or 0
        total_contracts = self.session.query(func.count(ContractTable.contract_id)).filter(
            ContractTable.user_id == self.user_id
        ).scalar() or 0
        total_products = self.session.query(func.count(ProductTable.product_id)).filter(
            ProductTable.user_id == self.user_id
        ).scalar() or 0

        total_sales = float(
            self.session.query(
                func.coalesce(
                    func.sum(ContractTable.sale_price - func.coalesce(ProductTable.product_price, 0)),
                    0,
                )
            )
            .outerjoin(ProductTable, ContractTable.product_id == ProductTable.product_id)
            .filter(ContractTable.user_id == self.user_id)
            .scalar() or 0
        )

        collected_amount = float(
            self.session.query(func.coalesce(func.sum(PayingTable.paid_amount), 0))
            .filter(PayingTable.user_id == self.user_id)
            .scalar() or 0
        )

        remaining_price_total = float(
            self.session.query(func.coalesce(func.sum(ContractTable.remaining_price), 0))
            .filter(ContractTable.user_id == self.user_id)
            .scalar() or 0
        )
        remaining_amount = remaining_price_total - collected_amount

        today = date.today()

        product_prices = dict(
            self.session.query(ProductTable.product_id, ProductTable.product_price)
            .filter(ProductTable.user_id == self.user_id)
            .all()
        )

        contracts = self.session.query(ContractTable).filter(ContractTable.user_id == self.user_id).all()

        todays_installments = 0
        overdue_installments = 0
        monthly_profit = 0.0
        monthly_expected_amount = 0.0

        for contract in contracts:
            due_installments = 0
            due_today = False
            due_this_month_count = 0

            for i in range(contract.installment_num):
                due_date = contract.first_installment + relativedelta(months=i)

                if due_date <= today:
                    due_installments += 1
                if due_date == today:
                    due_today = True
                if due_date.year == today.year and due_date.month == today.month:
                    due_this_month_count += 1

            if due_today:
                todays_installments += 1

            paid_for_contract = float(
                self.session.query(func.coalesce(func.sum(PayingTable.paid_amount), 0))
                .filter(PayingTable.contract_id == contract.contract_id, PayingTable.user_id == self.user_id)
                .scalar() or 0
            )
            installment_value = float(contract.installment_value) if contract.installment_value else 0
            paid_installments = int(paid_for_contract // installment_value) if installment_value else 0
            overdue_installments += max(0, due_installments - paid_installments)

            if due_this_month_count and contract.installment_num:
                product_price = float(product_prices.get(contract.product_id, 0) or 0)
                contract_profit = float(contract.sale_price) - product_price
                profit_per_installment = contract_profit / contract.installment_num
                monthly_profit += profit_per_installment * due_this_month_count

                monthly_expected_amount += installment_value * due_this_month_count

        return DashboardStats(
            total_clients=total_clients,
            total_contracts=total_contracts,
            total_products=total_products,
            total_sales=total_sales,
            collected_amount=collected_amount,
            remaining_amount=remaining_amount,
            todays_installments=todays_installments,
            overdue_installments=overdue_installments,
            monthly_profit=monthly_profit,
            monthly_expected_amount=monthly_expected_amount,
        )