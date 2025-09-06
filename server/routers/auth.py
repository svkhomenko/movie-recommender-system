from fastapi import APIRouter, status, HTTPException, Response
from models.user import UserCreate, UserId, User
from dependencies.session import SessionDep
from services import user as UserService, token as TokenService

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
