from typing import List
from flix.domainmodel.genre import Genre
from flix.domainmodel.actor import Actor
from flix.domainmodel.director import Director


class Movie:
    def __init__(self, title, release_year):
        if title == "" or type(title) is not str:
            self._title = None
        else:
            self._title = title.strip()
        if type(release_year) is not int or release_year < 1900:
            self._release_year = None
        else:
            self._release_year = release_year
        self._description: str = None
        self._director: Director = None
        self._actors: List[Actor] = list()
        self._genres: List[Genre] = list()
        self._runtime_minutes: int = 0

    @property
    def title(self) -> str:
        return self._title

    @property
    def release_year(self) -> int:
        return self._release_year

    @property
    def description(self) -> str:
        return self._description

    @property
    def director(self) -> Director:
        return self._director

    @property
    def actors(self):
        return self._actors

    @property
    def genres(self):
        return self._genres

    @property
    def runtime_minutes(self) -> int:
        return self._runtime_minutes

    @title.setter
    def title(self, title):
        if title != "" and type(title) is str:
            self._title = title.strip()

    @release_year.setter
    def release_year(self, year):
        if type(year) is int and year >= 1900:
            self._release_year = year

    @description.setter
    def description(self, desc):
        if desc != "" and type(desc) is str:
            self._description = desc.strip()

    @director.setter
    def director(self, director):
        if type(director) is Director:
            self._director = director

    @actors.setter
    def actors(self, actors):
        if type(actors) is List[Actor]:
            self._actors = actors

    @genres.setter
    def genres(self, genres):
        if type(genres) is List[Genre]:
            self._genres = genres

    @runtime_minutes.setter
    def runtime_minutes(self, runtime):
        if type(runtime) is int:
            if runtime > 0:
                self._runtime_minutes = runtime
            else:
                raise ValueError()

    def __repr__(self):
        return f"<Movie {self._title}, {self._release_year}>"

    def __eq__(self, other):
        if not isinstance(other, Movie):
            return False
        else:
            return other._title == self._title and other._release_year == self._release_year

    def __lt__(self, other):
        if self._title != other._title:
            return self._title < other._title
        else:
            return self._release_year < other._release_year

    def __hash__(self):
        hash_string = self._title + str(self._release_year)
        return hash(hash_string)

    def add_actor(self, actor):
        if type(actor) is Actor:
            self._actors.append(actor)

    def remove_actor(self, actor):
        if actor in self._actors:
            self._actors.remove(actor)

    def add_genre(self, genre):
        if type(genre) is Genre:
            self._genres.append(genre)

    def remove_genre(self, genre):
        if genre in self._genres:
            self._genres.remove(genre)
