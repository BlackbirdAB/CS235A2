import pytest

import flix.utilities.services as services
from flix.adapters.memory_repository import MemoryRepository
from flix.domainmodel.actor import Actor
from flix.domainmodel.director import Director
from flix.domainmodel.genre import Genre
from flix.domainmodel.movie import Movie
from flix.domainmodel.review import Review
from flix.domainmodel.user import User


@pytest.fixture()
def repository():
    repo = MemoryRepository()
    user1 = User("Myles Kennedy", "123")
    user2 = User("Mark Tremonti", "456")
    director1 = Director("Taika Waititi")
    director2 = Director("Steven Speilberg")
    actor1 = Actor("Chris Pratt")
    actor2 = Actor("Emma Watson")
    actor3 = Actor("Tom Hanks")
    genre1 = Genre("Comedy")
    genre2 = Genre("Animation")
    movie1 = Movie("Moana", 2016)
    movie2 = Movie("Ice Age", 2002)
    movie1.director = director1
    movie2.director = director2
    movie1.add_actor(actor1)
    movie2.add_actor(actor2)
    movie2.add_actor(actor3)
    actor2.add_actor_colleague(actor3)
    actor3.add_actor_colleague(actor2)
    movie1.add_genre(genre1)
    movie2.add_genre(genre2)
    review1 = Review(movie1, "very nice", 9)
    review2 = Review(movie2, "incredible", 10)
    user1.add_review(review1)
    user2.add_review(review2)
    repo.add_movie(movie1)
    repo.add_movie(movie2)
    repo.add_director(director1)
    repo.add_director(director2)
    repo.add_actor(actor1)
    repo.add_actor(actor2)
    repo.add_genre(genre1)
    repo.add_genre(genre2)
    repo.add_review(review1)
    repo.add_review(review2)
    repo.add_user(user1)
    repo.add_user(user2)
    return repo


def test_movies_to_dict(repository):
    movie1 = repository.get_movie("Moana", 2016)
    movie2 = repository.get_movie("Ice Age", 2002)
    movie_dicts = services.movies_to_dict([movie2, movie1])
    assert movie_dicts[0]['title'] == "Ice Age" and movie_dicts[0]['release_year'] == 2002 and \
           movie_dicts[0]['director'] == "Steven Speilberg" and movie_dicts[0]['actors'][0] == "Emma Watson" and \
           movie_dicts[0]['genres'][0] == "Animation" and len(movie_dicts) == 2
    assert services.movie_to_dict("not a movie") is None


def test_get_random_movies(repository):
    random_movies = services.get_random_movies(1, repository)
    assert len(random_movies) == 1 and (random_movies[0]['title'] == "Moana" or random_movies[0]['title'] == "Ice Age")
    random_movies = services.get_random_movies(5, repository)
    assert len(random_movies) == 1


def test_get_user(repository):
    assert services.get_user("Myles Kennedy", repository) == User("Myles Kennedy", "123")
    with pytest.raises(services.UnknownUserException):
        services.get_user("Scott Phillips", repository)



