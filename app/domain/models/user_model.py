# domain/entities/user.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    user_id: Optional[int]
    google_sub: str
    email: str
    user_name: str
    picture_url: Optional[str]
    role: str
    balance: float
    is_active: bool
    created_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None