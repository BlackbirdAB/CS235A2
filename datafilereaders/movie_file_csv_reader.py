import csv
from typing import List
from flix.domainmodel.movie import Movie
from flix.domainmodel.actor import Actor
from flix.domainmodel.genre import Genre
from flix.domainmodel.director import Director


class MovieFileCSVReader:
    def __init__(self, file_name: str):
        self.__file_name: str = file_name
        self.__dataset_of_movies: List[Movie] = list()
        self.__dataset_of_actors: List[Actor] = list()
        self.__dataset_of_directors: List[Director] = list()
        self.__dataset_of_genres: List[Genre] = list()

    @property
    def dataset_of_movies(self):
        return self.__dataset_of_movies

    @property
    def dataset_of_actors(self):
        return self.__dataset_of_actors

    @property
    def dataset_of_directors(self):
        return self.__dataset_of_directors

    @property
    def dataset_of_genres(self):
        return self.__dataset_of_genres

    def read_csv_file(self):
        with open(self.__file_name, newline="", encoding="utf-8-sig") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                movie = Movie(row["Title"], int(row["Year"]))
                movie.description = row["Description"]
                movie.runtime_minutes = int(row["Runtime (Minutes)"])
                if movie not in self.__dataset_of_movies:
                    self.__dataset_of_movies.append(movie)
                actors = row["Actors"].split(",")
                for actor in actors:
                    actor_true = Actor(actor.strip())
                    if actor_true not in self.__dataset_of_actors:
                        self.__dataset_of_actors.append(actor_true)
                    movie.add_actor(actor_true)
                director = Director(row["Director"])
                movie.director = director
                if director not in self.__dataset_of_directors:
                    self.__dataset_of_directors.append(director)
                genres = row["Genre"].split(",")
                for genre in genres:
                    genre_true = Genre(genre.strip())
                    if genre_true not in self.__dataset_of_genres:
                        self.__dataset_of_genres.append(genre_true)
                    movie.add_genre(genre_true)
