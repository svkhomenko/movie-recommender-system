from sqlmodel import Session, select
from models.user import User
from models.rating import Rating


def create_or_update(session: Session, movie_id: int, cur_user: User, rating: int):
    rating_obj = session.exec(
        select(Rating)
        .where(Rating.user_id == cur_user.id, Rating.movie_id == movie_id)
        .limit(1)
    ).first()

    if rating_obj:
        rating_obj.rating = rating
    else:
        rating_obj = Rating(user_id=cur_user.id, movie_id=movie_id, rating=rating)

    session.add(rating_obj)
    session.commit()
    session.refresh(rating_obj)

    return rating_obj


def delete(session: Session, movie_id: int, cur_user: User):
    rating_obj = session.exec(
        select(Rating)
        .where(Rating.user_id == cur_user.id, Rating.movie_id == movie_id)
        .limit(1)
    ).first()

    if rating_obj:
        session.delete(rating_obj)
        session.commit()
