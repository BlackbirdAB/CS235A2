import os

from typing import List

from bisect import insort_left

from werkzeug.security import generate_password_hash

from flix.adapters.repository import AbstractRepository
from flix.domainmodel.movie import Movie
from flix.domainmodel.user import User
from flix.domainmodel.director import Director
from flix.domainmodel.actor import Actor
from flix.domainmodel.genre import Genre
from flix.domainmodel.review import Review
from datafilereaders.movie_file_csv_reader import MovieFileCSVReader


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self._movies = list()
        self._directors = list()
        self._genres = list()
        self._users = list()
        self._reviews = list()
        self._actors = list()

    def add_director(self, director: Director):
        if type(director) is Director and director not in self._directors:
            insort_left(self._directors, director)

    def get_director(self, name: str):
        for director in self._directors:
            if director.director_full_name == name:
                return director
        return None

    def get_directors_by_name(self, name: str) -> List[Director]:
        directors = []
        if type(name) is str:
            try:
                name = name.strip().lower()
                for director in self._directors:
                    d_name = director.director_full_name.strip().lower()
                    if name in d_name:
                        if name == d_name[0: len(name)]:
                            i = 0
                            if len(directors) > 0:
                                while directors[i].director_full_name.lower().strip()[0: len(name)] == name:
                                    i += 1
                                    if i >= len(directors):
                                        break
                            directors.insert(i, director)
                        else:
                            directors.append(director)
            except ValueError:
                pass
        return directors

    def add_actor(self, actor: Actor):
        if type(actor) is Actor and actor not in self._actors:
            insort_left(self._actors, actor)

    def get_actor(self, name: str):
        for actor in self._actors:
            if actor.actor_full_name == name:
                return actor
        return None

    def get_actors_by_name(self, name: str) -> List[Actor]:
        actors = []
        if type(name) is str:
            try:
                name = name.strip().lower()
                for actor in self._actors:
                    a_name = actor.actor_full_name.strip().lower()
                    if name in a_name:
                        if name == a_name[0: len(name)]:
                            i = 0
                            if len(actors) > 0:
                                while actors[i].actor_full_name.lower().strip()[0: len(name)] == name:
                                    i += 1
                                    if i >= len(actors):
                                        break
                            actors.insert(i, actor)
                        else:
                            actors.append(actor)
            except ValueError:
                pass
        return actors

    def add_user(self, user: User):
        if type(user) is User and user not in self._users:
            self._users.append(user)

    def get_user(self, username):
        target_user = User(username, "abc")
        for user in self._users:
            if user == target_user:
                return user
        return None

    def get_users(self) -> List[User]:
        return self._users

    def add_movie(self, movie: Movie):
        if type(movie) is Movie and movie not in self._movies:
            insort_left(self._movies, movie)

    def get_movie(self, title: str, release_year: int):
        try:
            movie = Movie(title, release_year)
            if movie in self._movies:
                return self._movies[self._movies.index(movie)]

        except KeyError:
            pass  # Ignore exception and return None.

        return None

    def get_movies(self):
        return self._movies

    def get_movies_by_title(self, target_title: str) -> List[Movie]:
        movies = []
        if type(target_title) is str:
            try:
                name = target_title.strip().lower()
                for movie in self._movies:
                    m_name = movie.title.strip().lower()
                    if name in m_name:
                        if name == m_name[0: len(name)]:
                            i = 0
                            if len(movies) > 0:
                                while movies[i].title.lower().strip()[0: len(name)] == name:
                                    i += 1
                                    if i >= len(movies):
                                        break
                            movies.insert(i, movie)
                        else:
                            movies.append(movie)
            except ValueError:
                # No movies for specified title. Simply return an empty list.
                pass

        return movies

    def get_movies_by_director(self, target_director: str) -> List[Movie]:
        matching_movies = list()
        if type(target_director) is str:
            try:
                for movie in self._movies:
                    if target_director == movie.director.director_full_name:
                        matching_movies.append(movie)
            except ValueError:
                # No movies for specified director. Simply return an empty list.
                pass

        return matching_movies

    def get_movies_by_actor(self, target_actor: str) -> List[Movie]:
        matching_movies = list()
        if type(target_actor) is str:
            try:
                for movie in self._movies:
                    for actor in movie.actors:
                        if target_actor == actor.actor_full_name:
                            matching_movies.append(movie)
                            break
            except ValueError:
                # No movies for specified actor. Simply return an empty list.
                pass

        return matching_movies

    def get_movies_by_genre(self, target_genre: str) -> List[Movie]:
        matching_movies = list()
        if type(target_genre) is str:
            try:
                for movie in self._movies:
                    for genre in movie.genres:
                        if target_genre == genre.genre_name:
                            matching_movies.append(movie)
                            break
            except ValueError:
                # No movies for specified genre. Simply return an empty list.
                pass

        return matching_movies

    def get_number_of_movies(self):
        return len(self._movies)

    def add_genre(self, genre: Genre):
        if type(genre) is Genre and genre not in self._genres:
            insort_left(self._genres, genre)

    def get_genres(self) -> List[Genre]:
        return self._genres

    def add_review(self, review: Review):
        if type(review) is Review and review not in self._reviews:
            self._reviews.append(review)

    def get_reviews(self):
        return self._reviews


def load_data(data_path: str, repo: MemoryRepository):
    reader = MovieFileCSVReader(os.path.join(data_path, 'data1000Movies.csv'))
    reader.read_csv_file()
    for actor in reader.dataset_of_actors:
        repo.add_actor(actor)
    for movie in reader.dataset_of_movies:
        repo.add_movie(movie)
        for actor in movie.actors:
            for colleague in movie.actors:
                if not actor.check_if_this_actor_worked_with(colleague) and actor != colleague:
                    actor.add_actor_colleague(colleague)
    for director in reader.dataset_of_directors:
        repo.add_director(director)
    for genre in reader.dataset_of_genres:
        repo.add_genre(genre)
    user = User(
        user_name="Myles Kennedy",
        password=generate_password_hash("123")
    )
    review = Review(repo.get_movie("Inception", 2010), "Absolutely incredible movie!", 10)
    repo.add_review(review)
    user.add_review(review)
    user.watchlist.add_movie(repo.get_movie("The Da Vinci Code", 2006))
    user.watchlist.add_movie(repo.get_movie("Moana", 2016))
    repo.add_user(user)
