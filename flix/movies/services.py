from typing import Iterable

from flask import session, redirect, url_for

from flix.adapters.repository import AbstractRepository
from flix.domainmodel.movie import Movie
from flix.domainmodel.review import Review


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def get_movie(title: str, release_year: int, repo: AbstractRepository):
    movie = repo.get_movie(title=title, release_year=release_year)
    return movie


def get_reviews_for_movie(movie: Movie, repo: AbstractRepository):
    reviews = repo.get_reviews()
    reviews_for_movie = list()
    for review in reviews:
        if review.movie == movie:
            reviews_for_movie.append(review)
    return reviews_to_dict(reviews_for_movie, repo)


def get_movies_by_title(title: str, repo: AbstractRepository):
    movies = repo.get_movies_by_title(target_title=title)
    return movies_to_dict(movies)


def get_movies_by_director(director: str, repo: AbstractRepository):
    movies = repo.get_movies_by_director(target_director=director)
    return movies_to_dict(movies)


def get_movies_by_actor(actor: str, repo: AbstractRepository):
    movies = repo.get_movies_by_actor(target_actor=actor)
    return movies_to_dict(movies)


def get_movies_by_genre(genre: str, repo: AbstractRepository):
    movies = repo.get_movies_by_genre(target_genre=genre)
    return movies_to_dict(movies)


def get_user(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    return user


def add_review(title: str, release_year: int, username: str, review_text: str, rating: int, repo: AbstractRepository):
    movie = repo.get_movie(title=title, release_year=release_year)
    if movie is None:
        raise NonExistentMovieException
    user = repo.get_user(username=username)
    if user is None:
        raise UnknownUserException
    review = Review(movie, review_text, rating)
    user.add_review(review)
    repo.add_review(review)


def review_to_dict(review: Review, repo: AbstractRepository):
    users = repo.get_users()
    target_user = None
    for user in users:
        if review in user.reviews:
            target_user = user
            break
    if target_user is not None and type(review) is Review:
        review_dict = {
            'movie_title': review.movie.title,
            'movie_release_year': review.movie.release_year,
            'user': target_user.user_name,
            'review_text': review.review_text,
            'rating': review.rating,
            'timestamp': review.timestamp
        }
        return review_dict
    return None


def reviews_to_dict(reviews: Iterable[Review], repo: AbstractRepository):
    return [review_to_dict(review, repo) for review in reviews]


def movie_to_dict(movie: Movie):
    if type(movie) is Movie:
        movie_dict = {
            'title': movie.title,
            'release_year': movie.release_year,
            'description': movie.description,
            'director': movie.director.director_full_name,
            'actors': [actor.actor_full_name for actor in movie.actors],
            'genres': [genre.genre_name for genre in movie.genres],
            'runtime_minutes': movie.runtime_minutes
        }
        return movie_dict
    return None


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]
