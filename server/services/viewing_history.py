from sqlmodel import Session, select
from models.viewing_history import ViewingHistory
from models.user import User


def add_viewing_history(session: Session, cur_user: User | None, movie_id: int):
    if cur_user and cur_user.id:
        viewing_history = ViewingHistory(user_id=cur_user.id, movie_id=movie_id)
        session.add(viewing_history)
        session.commit()
        session.refresh(viewing_history)


def delete_all(session: Session, movie_id: int, cur_user: User):
    viewing_history_list = session.exec(
        select(ViewingHistory).where(
            ViewingHistory.user_id == cur_user.id, ViewingHistory.movie_id == movie_id
        )
    ).all()

    if viewing_history_list:
        for entry in viewing_history_list:
            session.delete(entry)

        session.commit()
