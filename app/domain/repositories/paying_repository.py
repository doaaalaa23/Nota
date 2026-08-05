from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.paying_model import Paying


class PayingRepository(ABC):
    @abstractmethod
    def set_user_id(self, user_id: int) -> None:
        """Bind subsequent operations to the authenticated user."""
        pass

    @abstractmethod
    def create(self, paying: Paying) -> Paying:
        pass

    @abstractmethod
    def update(self, paying: Paying) -> Paying:
        pass
    @abstractmethod
    def read(self, paying_id: int) -> Optional[Paying]:
        pass

    @abstractmethod
    def read_all(self) -> List[Paying]:
        pass

    @abstractmethod
    def read_by_contract(self, contract_id: int) -> List[Paying]:
        pass

    @abstractmethod
    def delete(self, paying_id: int) -> bool:
        pass

    @abstractmethod
    def exists(self, paying_id: int) -> bool:
        pass
