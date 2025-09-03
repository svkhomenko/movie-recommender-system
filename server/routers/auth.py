from fastapi import APIRouter, status
from models.user import UserCreate, UserId
from dependencies.session import SessionDep
from services import user as UserService

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
