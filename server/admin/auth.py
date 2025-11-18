import os
from starlette.requests import Request
from sqladmin.authentication import AuthenticationBackend
from sqlmodel import Session
from database import engine
from sqlmodel import select
from models.user import User, UserRoleEnum
from services import (
    user as UserService,
    token as TokenService,
    password as PasswordService,
)


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        if not isinstance(username, str) or not isinstance(password, str):
            return False

        try:
            with Session(engine) as session:
                user = session.exec(
                    select(User).where(User.email == username).limit(1)
                ).first()

                if (
                    not user
                    or user.role != UserRoleEnum.ADMIN
                    or not PasswordService.compare_passwords(password, user.password)
                ):
                    return False

                if not user.is_active:
                    if user.id:
                        UserService.send_confirm_token_for_email(user.id, user.email)
                    return False

                access_token, _ = TokenService.generate_user_tokens({"id": user.id})

            request.session.update({"admin_jwt": access_token})
            return True

        except Exception:
            return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        jwt_token = request.session.get("admin_jwt")

        if not jwt_token:
            return False

        try:
            data = TokenService.validate(jwt_token)
            if not (isinstance(data, dict) and "id" in data):
                return False

            with Session(engine) as session:
                user = session.get(User, data["id"])
                if not user or user.role != UserRoleEnum.ADMIN:
                    return False

        except Exception:
            return False

        return True


authentication_backend = AdminAuth(secret_key=os.getenv("SESSION_SECRET", ""))
