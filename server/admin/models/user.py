from sqladmin import ModelView
from database import engine
from sqlmodel import Session, SQLModel
from sqladmin.filters import BooleanFilter, AllUniqueStringValuesFilter
from starlette.requests import Request
from pydantic import EmailStr
from models.user import User, UserCreate, UserRoleEnum
from services import (
    user as UserService,
    password as PasswordService,
)


class UserCreateValidate(UserCreate):
    role: UserRoleEnum


class UserUpdateValidate(SQLModel):
    email: EmailStr
    role: UserRoleEnum


class UserAdmin(ModelView, model=User):
    name = "User"
    name_plural = "Users"

    column_list = [
        "id",
        "email",
        "role",
        "is_active",
    ]
    column_details_list = [
        "id",
        "email",
        "role",
        "is_active",
    ]
    form_excluded_columns = [
        "viewing_history",
        "ratings",
        "watch_later",
        "watched",
    ]

    form_create_rules = ["email", "password", "role", "is_active"]
    form_edit_rules = ["email", "role", "is_active"]

    column_searchable_list = ["email"]
    column_sortable_list = ["id", "email", "role", "is_active"]

    user_table = getattr(User, "__table__", None)
    if user_table is not None:
        column_filters = [
            BooleanFilter(user_table.c.is_active),
            AllUniqueStringValuesFilter(user_table.c.role),
        ]

    async def on_model_change(self, data, model, is_created, request):
        if data["role"]:
            data["role"] = data["role"].lower()

        if is_created:
            UserCreateValidate.model_validate(data)
            data["password"] = PasswordService.hash_password(data["password"])

            email = data.get("email")
            if email and isinstance(email, str):
                with Session(engine) as session:
                    UserService.check_email(session, email)

        if not is_created:
            UserUpdateValidate.model_validate(data)

        if not is_created and model.email != data.get("email"):
            email = data.get("email")
            if email and isinstance(email, str):
                with Session(engine) as session:
                    UserService.check_email(session, email)

    def is_visible(self, request: Request) -> bool:
        return request.session.get("admin_jwt") is not None

    def is_accessible(self, request: Request) -> bool:
        return request.session.get("admin_jwt") is not None
