from fastapi import APIRouter, Depends, HTTPException, Header
from app.presentation.schemas.auth_schemas import GoogleTokenIn, BalanceIn, AuthResponse, UserOut, BalanceOut
from app.infrastructure.auth.google_verify import verify_google_token
from app.infrastructure.auth.jwt_utils import create_access_token, decode_access_token
from app.application.usecases.authenticate_with_google import AuthenticateWithGoogleUseCase
from app.application.usecases.set_user_balance import SetUserBalanceUseCase
from app.application.usecases.get_user_balance import GetUserBalanceUseCase
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.database.session import get_session

router = APIRouter(prefix="/api/auth", tags=["auth"])

def get_auth_use_case(session=Depends(get_session)) -> AuthenticateWithGoogleUseCase:
    return AuthenticateWithGoogleUseCase(user_repository=UserRepositoryImpl(session))

def get_balance_use_case(session=Depends(get_session)) -> GetUserBalanceUseCase:
    return GetUserBalanceUseCase(user_repository=UserRepositoryImpl(session))

def get_set_balance_use_case(session=Depends(get_session)) -> SetUserBalanceUseCase:
    return SetUserBalanceUseCase(user_repository=UserRepositoryImpl(session))

def get_current_user_id(authorization: str = Header(None)) -> int:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing or invalid authorization header")
    token = authorization.split(" ")[1]
    try:
        payload = decode_access_token(token)
    except Exception:
        raise HTTPException(401, "Invalid or expired token")
    return int(payload["sub"])


@router.post("/google", response_model=AuthResponse)
def authenticate_with_google(
    payload: GoogleTokenIn,
    use_case: AuthenticateWithGoogleUseCase = Depends(get_auth_use_case),
):
    try:
        idinfo = verify_google_token(payload.id_token)
        result = use_case.execute(idinfo)
    except ValueError as e:
        raise HTTPException(400, str(e))

    user = result["user"]
    token = create_access_token(user.user_id, user.role)
    return {
        "access_token": token,
        "is_new": result["is_new"],
        "user": {
            "user_id": user.user_id, "email": user.email, "user_name": user.user_name,
            "picture_url": user.picture_url, "role": user.role,
            "balance": user.balance, "is_active": user.is_active,
        },
    }


@router.put("/balance", response_model=UserOut)
def set_balance(
    payload: BalanceIn,
    user_id: int = Depends(get_current_user_id),
    use_case: SetUserBalanceUseCase = Depends(get_set_balance_use_case),
):
    try:
        user = use_case.execute(user_id, payload.balance)
    except ValueError as e:
        raise HTTPException(404, str(e))
    return {
        "user_id": user.user_id, "email": user.email, "user_name": user.user_name,
        "picture_url": user.picture_url, "role": user.role,
        "balance": user.balance, "is_active": user.is_active,
    }

@router.get("/users/{user_id}/balance", response_model=BalanceOut)
def get_user_balance(
    user_id: int,
    use_case: GetUserBalanceUseCase = Depends(get_balance_use_case),
):
    try:
        balance = use_case.execute(user_id=user_id)
    except ValueError as e:
        raise HTTPException(404, str(e))
    return BalanceOut(balance=balance)