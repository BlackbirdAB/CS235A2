import abc
from typing import List

from flix.domainmodel.actor import Actor
from flix.domainmodel.director import Director
from flix.domainmodel.genre import Genre
from flix.domainmodel.movie import Movie
from flix.domainmodel.review import Review
from flix.domainmodel.user import User


repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_director(self, director: Director):
        raise NotImplementedError

    @abc.abstractmethod
    def get_director(self, name: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_directors_by_name(self, name: str) -> List[Director]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_actor(self, actor: Actor):
        raise NotImplementedError

    @abc.abstractmethod
    def get_actor(self, name: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_actors_by_name(self, name: str) -> List[Actor]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username):
        raise NotImplementedError

    @abc.abstractmethod
    def get_users(self) -> List[User]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, title: str, release_year: int) -> Movie:
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_title(self, target_title: str) -> List[Movie]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_director(self, target_director: str) -> List[Movie]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_actor(self, target_actor: str) -> List[Movie]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_genre(self, target_genre: str) -> List[Movie]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movies(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews(self):
        raise NotImplementedError
