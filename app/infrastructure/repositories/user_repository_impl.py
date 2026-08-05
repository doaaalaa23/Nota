from typing import Optional
from datetime import datetime
from app.domain.repositories.user_repository import UserRepository
from app.domain.models.user_model import User
from app.infrastructure.models.user_model import UserTable

class UserRepositoryImpl(UserRepository):
    def __init__(self, session):
        self.session = session

    def _to_entity(self, row: UserTable) -> User:
        return User(
            user_id=row.user_id, google_sub=row.google_sub, email=row.email, user_name=row.user_name,
            picture_url=row.picture_url, role=row.role, balance=float(row.balance),
            is_active=row.is_active, created_at=row.created_at, last_login_at=row.last_login_at,
        )

    def get_by_google_sub(self, google_sub: str) -> Optional[User]:
        row = self.session.query(UserTable).filter(UserTable.google_sub == google_sub).first()
        return self._to_entity(row) if row else None

    def get_by_id(self, user_id: int) -> Optional[User]:
        row = self.session.query(UserTable).filter(UserTable.user_id == user_id).first()
        return self._to_entity(row) if row else None

    def create(self, google_sub, email, user_name, picture_url, role="staff", balance=0.0) -> User:
        row = UserTable(
            google_sub=google_sub, email=email, user_name=user_name, picture_url=picture_url,
            role=role, balance=balance, is_active=True, created_at=datetime.utcnow(),
        )
        self.session.add(row)
        self.session.commit()
        self.session.refresh(row)
        return self._to_entity(row)

    def update_last_login(self, user_id: int) -> None:
        row = self.session.query(UserTable).filter(UserTable.user_id == user_id).first()
        if row:
            row.last_login_at = datetime.utcnow()
            self.session.commit()

    def update_balance(self, user_id: int, balance: float) -> User:
        row = self.session.query(UserTable).filter(UserTable.user_id == user_id).first()
        if not row:
            raise ValueError("User not found")
        row.balance = balance
        self.session.commit()
        self.session.refresh(row)
        return self._to_entity(row)

    def get_balance(self, user_id: int) -> float:
        row = self.session.query(UserTable).filter(UserTable.user_id == user_id).first()
        if not row:
            raise ValueError("User not found")
        return float(row.balance)