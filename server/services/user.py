from fastapi import HTTPException, status
from sqlmodel import Session, select
from models.user import UserCreate, User
from .password import hash_password
from .token import generate_confirm_token
from .email import send_mail
from consts.email import EMAIL_CONFIRM


def check_email(session: Session, email: str, id: int = 0):
    user = session.exec(
        select(User).where(User.email == email, User.id != id).limit(1)
    ).first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists",
        )


def send_confirm_token_for_email(id: int, email: str):
    token = generate_confirm_token({"id": id})
    send_mail(email, EMAIL_CONFIRM, {"token": token})


def create(session: Session, data: UserCreate):
    check_email(session, data.email)

    data.password = hash_password(data.password)

    user = User.model_validate(data)
    session.add(user)
    session.commit()
    session.refresh(user)

    if user.id:
        send_confirm_token_for_email(user.id, user.email)

    return user
