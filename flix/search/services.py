from typing import Iterable

from flask import url_for

from flix.adapters.repository import AbstractRepository
from flix.domainmodel.actor import Actor
from flix.domainmodel.director import Director
from flix.domainmodel.genre import Genre


def get_directors_by_name(name: str, repo: AbstractRepository):
    return directors_to_dict(repo.get_directors_by_name(name))


def get_actors_by_name(name: str, repo: AbstractRepository):
    return actors_to_dict(repo.get_actors_by_name(name))


def get_genres(repo: AbstractRepository):
    return genres_to_dict(repo.get_genres())


def get_colleagues(actor_name: str, repo: AbstractRepository):
    actor = repo.get_actor(actor_name)
    if actor is not None:
        return actors_to_dict(actor.colleagues)
    return None


def director_to_dict(director: Director):
    if type(director) is Director:
        director_dict = {
            'name': director.director_full_name,
        }
        return director_dict
    return None


def actor_to_dict(actor: Actor):
    if type(actor) is Actor:
        actor_dict = {
            'name': actor.actor_full_name
        }
        return actor_dict
    return None


def genre_to_dict(genre: Genre):
    if type(genre) is Genre:
        genre_dict = {
            'name': genre.genre_name
        }
        return genre_dict
    return None


def directors_to_dict(directors: Iterable[Director]):
    return [director_to_dict(director) for director in directors]


def actors_to_dict(actors: Iterable[Actor]):
    return [actor_to_dict(actor) for actor in actors]


def genres_to_dict(genres: Iterable[Genre]):
    return [genre_to_dict(genre) for genre in genres]
