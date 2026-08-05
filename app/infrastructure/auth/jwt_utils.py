from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import jwt
import os

load_dotenv()

SECRET_KEY = os.getenv("APP_JWT_SECRET")
if not SECRET_KEY:
    raise RuntimeError("Missing APP_JWT_SECRET environment variable.")
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60 * 12

def create_access_token(user_id: int, role: str) -> str:
    payload = {"sub": str(user_id), "role": role,
               "exp": datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])