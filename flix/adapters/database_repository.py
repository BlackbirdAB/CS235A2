import os

from typing import List

from sqlalchemy import asc
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from flix.adapters.repository import AbstractRepository
from flix.domainmodel.actor import Actor
from flix.domainmodel.director import Director
from flix.domainmodel.genre import Genre
from flix.domainmodel.movie import Movie
from flix.domainmodel.review import Review
from flix.domainmodel.user import User

tags = None


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_director(self, director: Director):
        if type(director) is Director:
            with self._session_cm as scm:
                scm.session.add(director)
                scm.commit()

    def get_director(self, name: str):
        director = None
        try:
            director = self._session_cm.session.query(Director).\
                filter_by(_director_full_name=name).one()
        except NoResultFound:
            pass
        return director

    def get_directors_by_name(self, name: str) -> List[Director]:
        if name is None:
            directors = self._session_cm.session.query(Director).all()
            return directors
        else:
            directors = self._session_cm.session.query(Director).\
                filter(Director._director_full_name.contains(name)).\
                order_by(asc(Director._director_full_name)).all()
            return directors

    def add_actor(self, actor: Actor):
        if type(actor) is Actor:
            with self._session_cm as scm:
                scm.session.add(actor)
                scm.commit()

    def get_actor(self, name: str):
        actor = None
        try:
            actor = self._session_cm.session.query(Actor).\
                filter_by(_actor_full_name=name).one()
        except NoResultFound:
            pass
        return actor

    def get_actors_by_name(self, name: str) -> List[Actor]:
        if name is None:
            actors = self._session_cm.session.query(Actor).all()
            return actors
        else:
            actors = self._session_cm.session.query(Actor). \
                filter(Actor._actor_full_name.contains(name)).\
                order_by(asc(Actor._actor_full_name)).all()
            return actors

    def add_user(self, user: User):
        with self._session_cm as scm:
            try:
                scm.session.add(user)
                scm.commit()
            except IntegrityError:
                pass

    def get_user(self, username):
        user = None
        try:
            user = self._session_cm.session.query(User).\
                filter_by(_user_name=username).one()
        except NoResultFound:
            pass
        return user

    def get_users(self) -> List[User]:
        users = self._session_cm.session.query(User).all()
        return users

    def add_movie(self, movie: Movie):
        if type(movie) is Movie:
            with self._session_cm as scm:
                scm.session.add(movie)
                scm.commit()

    def get_movie(self, title: str, release_year: int):
        movie = None
        try:
            movie = self._session_cm.session.query(Movie).filter(Movie._title == title).\
                filter(Movie._release_year == release_year).one()
        except NoResultFound:
            pass
        return movie

    def get_movies(self):
        movies = self._session_cm.session.query(Movie).order_by(asc(Movie._title)).all()
        return movies

    def get_movies_by_title(self, target_title: str) -> List[Movie]:
        if target_title is None:
            movies = []
            return movies
        else:
            movies = self._session_cm.session.query(Movie).\
                filter(Movie._title.contains(target_title)).\
                order_by(asc(Movie._title)).all()
            return movies

    def get_movies_by_director(self, target_director: str) -> List[Movie]:
        if target_director is None:
            directors = self._session_cm.session.query(Movie).all()
            return directors
        else:
            try:
                director = self._session_cm.session.query(Director).\
                    filter_by(_director_full_name=target_director).one()
                directors = self._session_cm.session.query(Movie).\
                    filter(Movie._director == director).\
                    order_by(asc(Movie._title)).all()
                return directors
            except NoResultFound:
                return []

    def get_movies_by_actor(self, target_actor: str) -> List[Movie]:
        if target_actor is None:
            actors = self._session_cm.session.query(Movie).all()
            return actors
        else:
            try:
                actor = self._session_cm.session.query(Actor). \
                    filter_by(_actor_full_name=target_actor).one()
                actors = self._session_cm.session.query(Movie). \
                    filter(Movie._actors.contains(actor)). \
                    order_by(asc(Movie._title)).all()
                return actors
            except NoResultFound:
                return []

    def get_movies_by_genre(self, target_genre: str) -> List[Movie]:
        if target_genre is None:
            genres = self._session_cm.session.query(Movie).all()
            return genres
        else:
            try:
                genre = self._session_cm.session.query(Genre). \
                    filter_by(_genre_name=target_genre).one()
                genres = self._session_cm.session.query(Movie). \
                    filter(Movie._genres.contains(genre)). \
                    order_by(asc(Movie._title)).all()
                return genres
            except NoResultFound:
                return []

    def get_number_of_movies(self):
        return self._session_cm.session.query(Movie).count()

    def add_genre(self, genre: Genre):
        if type(genre) is Genre:
            try:
                with self._session_cm as scm:
                    scm.session.add(genre)
                    scm.commit()
            except IntegrityError:
                pass

    def get_genres(self) -> List[Genre]:
        genres = self._session_cm.session.query(Genre).order_by(asc(Genre._genre_name)).all()
        return genres

    def add_review(self, review: Review):
        if type(review) is Review:
            with self._session_cm as scm:
                scm.session.add(review)
                scm.commit()

    def get_reviews(self):
        reviews = self._session_cm.session.query(Review).all()
        return reviews


def populate(engine: Engine, data_path: str):
    conn = engine.raw_connection()
    cursor = conn.cursor()

    reader = MovieFileCSVReader(os.path.join(data_path, 'data1000Movies.csv'))
    reader.read_csv_file()

    insert_directors = """INSERT INTO directors (name) VALUES (?)"""
    directors = []

    for director in reader.dataset_of_directors:
        director_tuple = tuple([director.director_full_name])
        directors.append(director_tuple)

    cursor.executemany(insert_directors, directors)

    insert_actors = """INSERT INTO actors (name) VALUES (?)"""
    actors = []

    for actor in reader.dataset_of_actors:
        actor_tuple = tuple([actor.actor_full_name])
        actors.append(actor_tuple)

    cursor.executemany(insert_actors, actors)

    insert_genres = """INSERT INTO genres (name) VALUES (?)"""
    genres = []

    for genre in reader.dataset_of_genres:
        genre_tuple = tuple([genre.genre_name])
        genres.append(genre_tuple)

    cursor.executemany(insert_genres, genres)

    insert_movies = """
            INSERT INTO movies (
            title, release_year, description, director_id, runtime_minutes)
            VALUES (?, ?, ?, ?, ?)"""
    movies = []

    for movie in reader.dataset_of_movies:
        movie_director_id = cursor.execute(
            'SELECT id FROM directors WHERE name = "' + movie.director.director_full_name + '"'
        ).fetchone()[0]
        movie_tuple = (movie.title, movie.release_year, movie.description, movie_director_id, movie.runtime_minutes)
        movies.append(movie_tuple)
    cursor.executemany(insert_movies, movies)

    insert_movie_actors = """INSERT INTO movie_actors (movie_id, actor_id) VALUES (?, ?)"""
    insert_movie_genres = """INSERT INTO movie_genres (movie_id, genre_id) VALUES (?, ?)"""
    insert_actor_colleagues = """INSERT INTO actor_colleagues (actor_id, colleague_id) VALUES (?, ?)"""
    movie_actors = []
    movie_genres = []
    actor_colleagues = []

    for movie in reader.dataset_of_movies:
        movie_id = cursor.execute(
            'SELECT id FROM movies '
            'WHERE title = "' + movie.title + '" AND release_year = "' + str(movie.release_year) + '"'
        ).fetchone()[0]

        for actor in movie.actors:
            actor_id = cursor.execute(
                'SELECT id FROM actors WHERE name = "' + actor.actor_full_name + '"'
            ).fetchone()[0]
            movie_actors.append((movie_id, actor_id))

            for colleague in movie.actors:
                if not actor.check_if_this_actor_worked_with(colleague) and actor != colleague:
                    colleague_id = cursor.execute(
                        'SELECT id FROM actors WHERE name = "' + colleague.actor_full_name + '"'
                    ).fetchone()[0]
                    actor_colleague_tuple = (actor_id, colleague_id)
                    actor_colleagues.append(actor_colleague_tuple)

        for genre in movie.genres:
            genre_id = cursor.execute(
                'SELECT id FROM genres WHERE name = "' + genre.genre_name + '"'
            ).fetchone()[0]
            movie_genres.append((movie_id, genre_id))

    cursor.executemany(insert_movie_actors, movie_actors)
    cursor.executemany(insert_movie_genres, movie_genres)
    cursor.executemany(insert_actor_colleagues, actor_colleagues)

    # user = User('Myles Kennedy', '123')
    # movie1 = Movie('Inception', 2010)
    # review = Review(movie1, "Absolutely incredible movie!", 10)
    # user.add_review(review)
    # movie2 = Movie("The Da Vinci Code", 2006)
    # user.watchlist.add_movie(movie1)
    # user.watchlist.add_movie(movie2)
    # cursor.execute(
    #     "INSERT INTO users (user_name, password, time_spent_watching_movies_minutes) VALUES (?, ?, 0)",
    #     (user.user_name, generate_password_hash(user.password))
    # )

    conn.commit()
    conn.close()
