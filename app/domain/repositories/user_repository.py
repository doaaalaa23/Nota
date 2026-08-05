from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models.user_model import User

class UserRepository(ABC):
    @abstractmethod
    def get_by_google_sub(self, google_sub: str) -> Optional[User]: ...

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]: ...

    @abstractmethod
    def create(self, google_sub: str, email: str, user_name: str,
               picture_url: Optional[str], role: str = "user",
               balance: float = 0.0) -> User: ...

    @abstractmethod
    def update_last_login(self, user_id: int) -> None: ...

    @abstractmethod
    def update_balance(self, user_id: int, balance: float) -> User: ...

    @abstractmethod
    def get_balance(self, user_id: int) -> float: ...