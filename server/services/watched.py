from sqlmodel import Session, select
from models.watched import Watched
from models.user import User
from datetime import datetime, timezone


def get_first(session: Session, movie_id: int, cur_user: User):
    return session.exec(
        select(Watched)
        .where(Watched.user_id == cur_user.id, Watched.movie_id == movie_id)
        .limit(1)
    ).first()


def create_or_update(session: Session, movie_id: int, cur_user: User):
    watched = get_first(session, movie_id, cur_user)

    if watched:
        watched.created_at = datetime.now(timezone.utc)
    else:
        watched = Watched(user_id=cur_user.id, movie_id=movie_id)

    session.add(watched)
    session.commit()
    session.refresh(watched)

    return watched


def delete(session: Session, movie_id: int, cur_user: User):
    watched = get_first(session, movie_id, cur_user)

    if watched:
        session.delete(watched)
        session.commit()
