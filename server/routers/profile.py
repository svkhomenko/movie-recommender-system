from fastapi import APIRouter, status, Response
from fastapi.responses import JSONResponse
from dependencies.session import SessionDep
from dependencies.current_user import CurrentUserDep
from models.user import UserUpdate, UserIsActive
from services import user as UserService


router = APIRouter(prefix="/profile", tags=["profile"])


@router.put(
    "/",
    response_model=UserIsActive,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"description": "The user with this email already exists"},
        401: {"description": "The access token is invalid or has expired"},
    },
)
async def update_profile(
    user_data: UserUpdate, cur_user: CurrentUserDep, session: SessionDep
):
    UserService.update(session, cur_user, user_data)

    response = JSONResponse(content={"is_active": cur_user.is_active})

    if not cur_user.is_active:
        response.delete_cookie("refreshToken")

    response.status_code = status.HTTP_201_CREATED
    return response


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={401: {"description": "The access token is invalid or has expired"}},
)
async def delete_profile(cur_user: CurrentUserDep, session: SessionDep):
    cur_user.is_active = False
    session.add(cur_user)
    session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
