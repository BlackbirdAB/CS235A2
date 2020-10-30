from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from flix.domainmodel.actor import Actor
from flix.domainmodel.director import Director
from flix.domainmodel.genre import Genre
from flix.domainmodel.movie import Movie
from flix.domainmodel.review import Review
from flix.domainmodel.user import User
from flix.domainmodel.watchlist import WatchList

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False),
    Column('time_spent_watching_movies_minutes', Integer, nullable=False),
    Column('watchlist_id', ForeignKey('watchlists.id'))
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('movie_id', ForeignKey('movies.id')),
    Column('review_text', String(1024), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('release_year', Integer, nullable=False),
    Column('description', String(1024), nullable=False),
    Column('director_id', ForeignKey('directors.id')),
    Column('runtime_minutes', Integer, nullable=False)
)

genres = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), unique=True, nullable=False)
)

directors = Table(
    'directors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), unique=True, nullable=False)
)

actors = Table(
    'actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), unique=True, nullable=False)
)

actor_colleagues = Table(
    'actor_colleagues', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('actor_id', ForeignKey('actors.id')),
    Column('colleague_id', ForeignKey('actors.id'))
)

movie_actors = Table(
    'movie_actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('actor_id', ForeignKey('actors.id'))
)

movie_genres = Table(
    'movie_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('genre_id', ForeignKey('genres.id'))
)

user_watched_movies = Table(
    'user_watched_movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('movie_id', ForeignKey('movies.id'))
)

watchlist_movies = Table(
    'watchlist_movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('watchlist_id', ForeignKey('watchlists.id')),
    Column('movie_id', ForeignKey('movies.id'))
)

watchlists = Table(
    'watchlists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True)
)


def map_model_to_tables():
    mapper(Review, reviews, properties={
        '_movie': relationship(Movie),
        '_review_text': reviews.c.review_text,
        '_rating': reviews.c.rating,
        '_timestamp': reviews.c.timestamp
    })
    genres_mapper = mapper(Genre, genres, properties={
        '_genre_name': genres.c.name
    })
    mapper(Director, directors, properties={
        '_director_full_name': directors.c.name
    })
    actors_mapper = mapper(Actor, actors, properties={
        '_actor_full_name': actors.c.name,
        '_colleagues': relationship(Actor, actor_colleagues, foreign_keys=[actor_colleagues.c.actor_id])
    })
    movies_mapper = mapper(Movie, movies, properties={
        '_title': movies.c.title,
        '_release_year': movies.c.release_year,
        '_description': movies.c.description,
        '_director': relationship(Director),
        '_actors': relationship(
            actors_mapper,
            secondary=movie_actors,
            backref='_movies'
        ),
        '_genres': relationship(
            genres_mapper,
            secondary=movie_genres,
            backref='_genre'
        ),
        '_runtime_minutes': movies.c.runtime_minutes
    })
    mapper(User, users, properties={
        '_user_name': users.c.user_name,
        '_password': users.c.password,
        '_watched_movies': relationship(
            movies_mapper,
            secondary=user_watched_movies
        ),
        '_reviews': relationship(Review, backref='_user'),
        '_time_spent_watching_movies_minutes': users.c.time_spent_watching_movies_minutes,
        '_watchlist': relationship(WatchList)
    })
    mapper(WatchList, watchlists, properties={
        '_watch_list': relationship(
            movies_mapper,
            secondary=watchlist_movies
        )
    })
