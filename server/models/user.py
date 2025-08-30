from sqlmodel import Field, SQLModel, Column, Enum, Relationship
from pydantic import EmailStr
import enum
from typing import TYPE_CHECKING
from ..consts.validation import PASSWORD_LENGTH

if TYPE_CHECKING:
    from .viewing_history import ViewingHistory
    from .rating import Rating
    from .watch_later import WatchLater
    from .watched import Watched


class UserRoleEnum(enum.Enum):
    USER = "user"
    ADMIN = "admin"


# id
# email
# password
# role
# is_active


# class UserBase(SQLModel):
#     pass


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field()
    password: str = Field()
    role: UserRoleEnum = Field(
        sa_column=Column(Enum(UserRoleEnum)), default=UserRoleEnum.USER
    )
    is_active: bool = Field(default=False)

    viewing_history: list["ViewingHistory"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    ratings: list["Rating"] = Relationship(back_populates="user", cascade_delete=True)
    watch_later: list["WatchLater"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    watched: list["Watched"] = Relationship(back_populates="user", cascade_delete=True)


class UserCreate(SQLModel):
    email: EmailStr
    password: str = Field(
        min_length=PASSWORD_LENGTH["min"], max_length=PASSWORD_LENGTH["max"]
    )


# class UserPublic(UserBase):
#     pass


# class UserCreate(UserBase):
#     pass

# class UserUpdate(UserBase):
#     pass
