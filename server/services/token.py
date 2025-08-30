import jwt
from jwt.exceptions import InvalidTokenError
import os
from datetime import datetime, timedelta, timezone

ALGORITHM = "HS256"


def generate(payload: dict, expires_delta: timedelta | None = None):
    payload = payload.copy()
    expires_delta = expires_delta or timedelta(hours=24)

    payload.update({"exp": datetime.now(timezone.utc) + expires_delta})

    return jwt.encode(payload, os.getenv("TOKEN_SECRET_KEY"), algorithm=ALGORITHM)


def validate(token: str | None):
    try:
        return jwt.decode(
            token or "", os.getenv("TOKEN_SECRET_KEY"), algorithms=[ALGORITHM]
        )
    except InvalidTokenError:
        return


def generate_confirm_token(payload: dict):
    return generate(payload, timedelta(hours=1))


def generate_user_tokens(payload: dict):
    access_token = generate(payload)
    refresh_token = generate(payload, timedelta(days=7))
    return access_token, refresh_token
