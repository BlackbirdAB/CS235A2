from typing import List
from flix.domainmodel.genre import Genre
from flix.domainmodel.actor import Actor
from flix.domainmodel.director import Director


class Movie:
    def __init__(self, title, release_year):
        if title == "" or type(title) is not str:
            self.__title = None
        else:
            self.__title = title.strip()
        if type(release_year) is not int or release_year < 1900:
            self.__release_year = None
        else:
            self.__release_year = release_year
        self.__description: str = None
        self.__director: Director = None
        self.__actors: List[Actor] = list()
        self.__genres: List[Genre] = list()
        self.__runtime_minutes: int = 0

    @property
    def title(self) -> str:
        return self.__title

    @property
    def release_year(self) -> int:
        return self.__release_year

    @property
    def description(self) -> str:
        return self.__description

    @property
    def director(self) -> Director:
        return self.__director

    @property
    def actors(self):
        return self.__actors

    @property
    def genres(self):
        return self.__genres

    @property
    def runtime_minutes(self) -> int:
        return self.__runtime_minutes

    @title.setter
    def title(self, title):
        if title != "" and type(title) is str:
            self.__title = title.strip()

    @release_year.setter
    def release_year(self, year):
        if type(year) is int and year >= 1900:
            self.__release_year = year

    @description.setter
    def description(self, desc):
        if desc != "" and type(desc) is str:
            self.__description = desc.strip()

    @director.setter
    def director(self, director):
        if type(director) is Director:
            self.__director = director

    @actors.setter
    def actors(self, actors):
        if type(actors) is List[Actor]:
            self.__actors = actors

    @genres.setter
    def genres(self, genres):
        if type(genres) is List[Genre]:
            self.__genres = genres

    @runtime_minutes.setter
    def runtime_minutes(self, runtime):
        if type(runtime) is int:
            if runtime > 0:
                self.__runtime_minutes = runtime
            else:
                raise ValueError()

    def __repr__(self):
        return f"<Movie {self.__title}, {self.__release_year}>"

    def __eq__(self, other):
        if not isinstance(other, Movie):
            return False
        else:
            return other.__title == self.__title and other.__release_year == self.__release_year

    def __lt__(self, other):
        if self.__title != other.__title:
            return self.__title < other.__title
        else:
            return self.__release_year < other.__release_year

    def __hash__(self):
        hash_string = self.__title + str(self.__release_year)
        return hash(hash_string)

    def add_actor(self, actor):
        if type(actor) is Actor:
            self.__actors.append(actor)

    def remove_actor(self, actor):
        if actor in self.__actors:
            self.__actors.remove(actor)

    def add_genre(self, genre):
        if type(genre) is Genre:
            self.__genres.append(genre)

    def remove_genre(self, genre):
        if genre in self.__genres:
            self.__genres.remove(genre)
