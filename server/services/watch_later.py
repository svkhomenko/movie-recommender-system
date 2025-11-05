from sqlmodel import Session, select
from models.watch_later import WatchLater
from models.user import User


def get_first(session: Session, movie_id: int, cur_user: User):
    return session.exec(
        select(WatchLater)
        .where(WatchLater.user_id == cur_user.id, WatchLater.movie_id == movie_id)
        .limit(1)
    ).first()


def create_if_doesnt_exist(session: Session, movie_id: int, cur_user: User):
    watch_later = get_first(session, movie_id, cur_user)

    if not watch_later:
        watch_later = WatchLater(user_id=cur_user.id, movie_id=movie_id)

        session.add(watch_later)
        session.commit()
        session.refresh(watch_later)

    return watch_later


def delete(session: Session, movie_id: int, cur_user: User):
    watch_later = get_first(session, movie_id, cur_user)

    if watch_later:
        session.delete(watch_later)
        session.commit()
