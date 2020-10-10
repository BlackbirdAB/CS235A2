from typing import Iterable
import random

from flask import url_for, session

from flix.adapters.repository import AbstractRepository
from flix.domainmodel.movie import Movie


class UnknownUserException(Exception):
    pass


def get_random_movies(quantity, repo: AbstractRepository):
    movie_count = repo.get_number_of_movies()

    if quantity >= movie_count:

        quantity = movie_count - 1

    # Pick distinct and random movies.
    random_indexes = random.sample(range(0, movie_count - 1), quantity)
    random_movies = list()
    movies = repo.get_movies()
    for i in random_indexes:
        random_movies.append(movies[i])

    return movies_to_dict(random_movies)


def get_user(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    return user


def get_watchlist_empty(repo: AbstractRepository):
    if 'username' in session:
        watchlist_empty = True
        username = session['username']
        try:
            user = get_user(username, repo)
            if user.watchlist.size() > 0:
                watchlist_empty = False
            return watchlist_empty
        except UnknownUserException:
            return watchlist_empty
    else:
        return True


# ============================================
# Functions to convert dicts to model entities
# ============================================

def movie_to_dict(movie: Movie):
    if type(movie) is Movie:
        movie_dict = {
            'title': movie.title,
            'release_year': movie.release_year,
            'description': movie.description,
            'director': movie.director.director_full_name,
            'actors': [actor.actor_full_name for actor in movie.actors],
            'genres': [genre.genre_name for genre in movie.genres],
            'runtime_minutes': movie.runtime_minutes,
        }
        return movie_dict
    return None


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]
