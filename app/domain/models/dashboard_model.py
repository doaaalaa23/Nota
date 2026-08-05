from dataclasses import dataclass


@dataclass
class DashboardStats:
    total_clients: int
    total_contracts: int
    total_products: int
    total_sales: float
    collected_amount: float
    remaining_amount: float
    todays_installments: int
    overdue_installments: int
    monthly_profit: float
    monthly_expected_amount: float
