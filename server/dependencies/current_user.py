from fastapi import Depends, HTTPException, status, Query
from typing import Annotated
from models.user import User
from models.movie import MoviePublicResultType, MoviePublicFilterSearchParams
from dependencies.oauth2 import oauth2_scheme, oauth2_scheme_optional
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


def get_optional_current_user(
    token: Annotated[str | None, Depends(oauth2_scheme_optional)], session: SessionDep
):
    data = TokenService.validate(token)
    if not (isinstance(data, dict) and "id" in data):
        return

    return session.get(User, data["id"])


def get_current_user_for_personal_lists(
    token: Annotated[str | None, Depends(oauth2_scheme_optional)],
    session: SessionDep,
    query: Annotated[MoviePublicFilterSearchParams, Query()],
):
    if (
        query.result_type == MoviePublicResultType.CONTINUE_WATCHING
        or query.result_type == MoviePublicResultType.RECOMMENDATIONS
        or query.result_type == MoviePublicResultType.WATCH_LATER
        or query.result_type == MoviePublicResultType.WATCHED
        or query.result_type == MoviePublicResultType.OWN_RATING
    ):
        if token:
            return get_current_user(token, session)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The access token is invalid or has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )


CurrentUserDep = Annotated[User, Depends(get_current_user)]
OptionalCurrentUserDep = Annotated[User | None, Depends(get_optional_current_user)]
CurrentUserForPersonalListsDep = Annotated[
    User | None, Depends(get_current_user_for_personal_lists)
]
