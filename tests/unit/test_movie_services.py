import pytest

import flix.movies.services as services
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
    genre1 = Genre("Comedy")
    genre2 = Genre("Animation")
    movie1 = Movie("Moana", 2016)
    movie2 = Movie("Ice Age", 2002)
    movie1.director = director1
    movie2.director = director2
    movie1.add_actor(actor1)
    movie2.add_actor(actor2)
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


def test_reviews_to_dict(repository):
    review_dicts = services.reviews_to_dict(repository.get_reviews(), repository)
    assert review_dicts[0]['movie_title'] == "Moana" and review_dicts[0]['movie_release_year'] == 2016 and \
           review_dicts[0]['user'] == "myles kennedy" and review_dicts[0]['review_text'] == "very nice" and \
           review_dicts[0]['rating'] == 9 and len(review_dicts) == 2
    review3 = Review(services.get_movie("Moana", 2016, repository), "Not my favourite.", 4)
    assert services.review_to_dict(review3, repository) is None
    assert services.review_to_dict("not a review", repository) is None


def test_movies_to_dict(repository):
    movie1 = repository.get_movie("Moana", 2016)
    movie2 = repository.get_movie("Ice Age", 2002)
    movie_dicts = services.movies_to_dict([movie2, movie1])
    assert movie_dicts[0]['title'] == "Ice Age" and movie_dicts[0]['release_year'] == 2002 and \
           movie_dicts[0]['director'] == "Steven Speilberg" and movie_dicts[0]['actors'][0] == "Emma Watson" and \
           movie_dicts[0]['genres'][0] == "Animation" and len(movie_dicts) == 2
    assert services.movie_to_dict("not a movie") is None


def test_get_movie(repository):
    assert services.get_movie("Moana", 2016, repository) == Movie("Moana", 2016)
    assert services.get_movie("A Silent Voice", 2016, repository) is None


def test_get_reviews_for_movie(repository):
    assert services.get_reviews_for_movie(Movie("Moana", 2016), repository)[0]['review_text'] == "very nice"
    assert services.get_reviews_for_movie(Movie("Moana", 2016), repository)[0]['rating'] == 9
    assert services.get_reviews_for_movie(Movie("A Silent Voice", 2016), repository) == []


def test_get_movies_by_title(repository):
    assert services.get_movies_by_title("Moana", repository)[0]['title'] == "Moana"
    assert services.get_movies_by_title("Moana", repository)[0]['release_year'] == 2016
    assert services.get_movies_by_title("A Silent Voice", repository) == []


def test_get_movies_by_director(repository):
    assert services.get_movies_by_director("Taika Waititi", repository)[0]['title'] == "Moana"
    assert services.get_movies_by_director("Taika Waititi", repository)[0]['release_year'] == 2016
    assert services.get_movies_by_director("James Cameron", repository) == []


def test_get_movies_by_actor(repository):
    assert services.get_movies_by_actor("Chris Pratt", repository)[0]['title'] == "Moana"
    assert services.get_movies_by_actor("Chris Pratt", repository)[0]['release_year'] == 2016
    assert services.get_movies_by_actor("Keanu Reeves", repository) == []


def test_get_movies_by_genre(repository):
    assert services.get_movies_by_genre("Comedy", repository)[0]['title'] == "Moana"
    assert services.get_movies_by_genre("Comedy", repository)[0]['release_year'] == 2016
    assert services.get_movies_by_genre("Action", repository) == []


def test_get_user(repository):
    assert services.get_user("Myles Kennedy", repository) == User("Myles Kennedy", "123")
    with pytest.raises(services.UnknownUserException):
        services.get_user("Scott Phillips", repository)


def test_add_review(repository):
    assert len(services.get_user("Mark Tremonti", repository).reviews) == 1
    assert len(repository.get_reviews()) == 2
    services.add_review("Moana", 2016, "Mark Tremonti", "Not my favourite.", 4, repository)
    assert len(services.get_user("Mark Tremonti", repository).reviews) == 2
    assert len(repository.get_reviews()) == 3
    with pytest.raises(services.NonExistentMovieException):
        services.add_review("A Silent Voice", 2016, "Mark Tremonti", "Not my favourite.", 4, repository)
    with pytest.raises(services.UnknownUserException):
        services.add_review("Moana", 2016, "Scott Phillips", "Not my favourite.", 4, repository)
