from dataclasses import dataclass
from app.domain.repositories.user_repository import UserRepository

@dataclass
class AuthenticateWithGoogleUseCase:
    user_repository: UserRepository

    def execute(self, idinfo: dict) -> dict:
        user = self.user_repository.get_by_google_sub(idinfo["sub"])
        is_new = False

        if user is None:
            user = self.user_repository.create(
                google_sub=idinfo["sub"],
                email=idinfo["email"],
                user_name=idinfo.get("name", idinfo["email"]),
                picture_url=idinfo.get("picture"),
                role="staff",
                balance=0.0,
            )
            is_new = True
        else:
            if not user.is_active:
                raise ValueError("This account has been disabled.")
            self.user_repository.update_last_login(user.user_id)

        return {"user": user, "is_new": is_new}