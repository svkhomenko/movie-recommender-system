from fastapi import Depends, HTTPException, status
from typing import Annotated
from models.user import User
from dependencies.oauth2 import oauth2_scheme
from dependencies.session import SessionDep
from services import token as TokenService


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep
):
    token_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="The access token is invalid or has expired",
        headers={"WWW-Authenticate": "Bearer"},
    )

    data = TokenService.validate(token)
    if not (isinstance(data, dict) and "id" in data):
        raise token_error

    user = session.get(User, data["id"])
    if not user:
        raise token_error

    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
