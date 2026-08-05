from fastapi import Header, HTTPException

from app.infrastructure.auth.jwt_utils import decode_access_token


def get_current_user_id(authorization: str = Header(None)) -> int:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing or invalid authorization header")

    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_access_token(token)
    except Exception as exc:
        raise HTTPException(401, "Invalid or expired token") from exc

    return int(payload["sub"])
