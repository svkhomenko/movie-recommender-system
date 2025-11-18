from markupsafe import Markup
from database import engine
from sqlmodel import Session
from enum import Enum
from models.movie import Movie
from models.crew import Crew


def _format_movies_details_view(model, attribute):
    movies_list = getattr(model, attribute)

    if not movies_list:
        return Markup(
            "<span class='badge bg-secondary'>There are no conected movies</span>"
        )

    result = []
    for movie in movies_list:
        movie_link = f"/admin/movie/details/{movie.id}"
        movie_data = f"""
                <div class="d-flex justify-content-start align-items-center p-1 border-bottom">
                    <span class="text-muted fw-bold me-3">Id: {movie.id}</span>
                    <a href="{movie_link}" target="_blank" class="text-decoration-none">{movie.title}</a>
                </div>
            """
        result.append(Markup(movie_data))

    return result


def _format_movie_crew_details_view(model, attribute):
    movie_crew_list = getattr(model, attribute)

    if not movie_crew_list:
        return Markup(
            "<span class='badge bg-secondary'>There are no conected movies</span>"
        )

    result = []

    for crew_link in movie_crew_list:
        with Session(engine) as session:
            movie = session.get(Movie, crew_link.movie_id)

        role = (
            crew_link.role.value if isinstance(crew_link.role, Enum) else crew_link.role
        )

        movie_link = f"/admin/movie/details/{crew_link.movie_id}"
        movie_data = f"""
            <div class="d-flex justify-content-start align-items-center p-1 border-bottom">
                <div class="d-flex align-items-center me-3">
                    <span class="text-muted fw-bold me-3">Id: {crew_link.movie_id}</span>
                    <a href="{movie_link}" target="_blank" class="text-decoration-none">{movie.title if movie else 'title'}</a>
                </div>
                <div>
                    <span class="badge bg-primary text-uppercase">{role}</span>
                </div>
            </div>
            """
        result.append(Markup(movie_data))

    return result


def _format_genres_collections_details_view(model, attribute):
    items = getattr(model, attribute)

    if not list:
        return Markup("<span class='badge bg-secondary'>Nothing found</span>")

    result = []
    for item in items:
        item_link = f"/admin/{attribute[:-1]}/details/{item.id}"
        item_data = f"""
                <div class="d-flex justify-content-start align-items-center p-1 border-bottom">
                    <span class="text-muted fw-bold me-3">Id: {item.id}</span>
                    <a href="{item_link}" target="_blank" class="text-decoration-none">{item.name}</a>
                </div>
            """
        result.append(Markup(item_data))

    return result


def _format_crew_movie_details_view(model, attribute):
    movie_crew_list = getattr(model, attribute)

    if not movie_crew_list:
        return Markup(
            "<span class='badge bg-secondary'>There are no conected crew members</span>"
        )

    result = []

    for movie_link in movie_crew_list:
        with Session(engine) as session:
            crew = session.get(Crew, movie_link.crew_id)

        role = (
            movie_link.role.value
            if isinstance(movie_link.role, Enum)
            else movie_link.role
        )

        crew_link = f"/admin/crew/details/{movie_link.crew_id}"
        crew_data = f"""
            <div class="d-flex justify-content-start align-items-center p-1 border-bottom">
                <div class="d-flex align-items-center me-3">
                    <span class="text-muted fw-bold me-3">Id: {movie_link.crew_id}</span>
                    <a href="{crew_link}" target="_blank" class="text-decoration-none">{crew.full_name if crew else 'full_name'}</a>
                </div>
                <div>
                    <span class="badge bg-primary text-uppercase">{role}</span>
                </div>
            </div>
            """
        result.append(Markup(crew_data))

    return result
