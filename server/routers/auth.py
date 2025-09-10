from fastapi import APIRouter, status, HTTPException, Response, Cookie
from sqlmodel import select
from models.user import UserCreate, UserId, User, UserLoginResponse, TokenResponse
from dependencies.session import SessionDep
from dependencies.oauth2 import OAuth2Dep
from services import (
    user as UserService,
    token as TokenService,
    password as PasswordService,
)
from consts.cookie import COOKIE_OPTIONS

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserId,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"description": "The user with this email already exists"}},
)
async def register(user_data: UserCreate, session: SessionDep):
    user = UserService.create(session, user_data)
    return {"id": user.id}


@router.post(
    "/confirm-email/{token}",
    responses={403: {"description": "The confirm token is invalid or has expired"}},
)
async def confirm_email(token: str, session: SessionDep):
    token_error = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="The confirm token is invalid or has expired",
    )

    data = TokenService.validate(token)
    if not (isinstance(data, dict) and "id" in data):
        raise token_error

    found = session.get(User, data["id"])
    if not found:
        raise token_error

    found.is_active = True
    session.add(found)
    session.commit()

    return Response(status_code=status.HTTP_200_OK)


@router.post(
    "/login",
    response_model=UserLoginResponse,
    responses={
        401: {"description": "Wrong username and/or password"},
        403: {"description": "Please confirm your email"},
    },
)
async def login(response: Response, form_data: OAuth2Dep, session: SessionDep):
    login_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Wrong username and/or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = session.exec(
        select(User).where(User.email == form_data.username).limit(1)
    ).first()

    if not user or not PasswordService.compare_passwords(
        form_data.password, user.password
    ):
        raise login_error

    if not user.is_active:
        if user.id:
            UserService.send_confirm_token_for_email(user.id, user.email)

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please confirm your email",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token, refresh_token = TokenService.generate_user_tokens({"id": user.id})

    response.set_cookie(key="refreshToken", value=refresh_token, **COOKIE_OPTIONS)

    return UserLoginResponse(
        access_token=access_token, token_type="bearer", **user.__dict__
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    responses={
        403: {"description": "The refresh token is invalid"},
        404: {"description": "No user found"},
    },
)
async def refresh(
    response: Response,
    session: SessionDep,
    refreshToken: str | None = Cookie(default=None),
):
    data = TokenService.validate(refreshToken)

    if not (isinstance(data, dict) and "id" in data):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The refresh token is invalid",
        )

    user = session.get(User, data["id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No user found",
        )

    access_token, refresh_token = TokenService.generate_user_tokens({"id": user.id})

    response.set_cookie(key="refreshToken", value=refresh_token, **COOKIE_OPTIONS)

    return TokenResponse(access_token=access_token, token_type="bearer")


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(response: Response):
    response.delete_cookie("refreshToken")
    response.status_code = status.HTTP_204_NO_CONTENT
    return response
