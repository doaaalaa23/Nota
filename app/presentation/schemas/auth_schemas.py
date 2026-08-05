from pydantic import BaseModel
from typing import Optional

class GoogleTokenIn(BaseModel):
    id_token: str

class BalanceIn(BaseModel):
    balance: float

class UserOut(BaseModel):
    user_id: int
    email: str
    user_name: str
    picture_url: Optional[str]
    role: str
    balance: float
    is_active: bool

class AuthResponse(BaseModel):
    access_token: str
    is_new: bool
    user: UserOut
  
class BalanceOut(BaseModel):
    balance: float