import pytest

import flix.search.services as services
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


def test_directors_to_dict(repository):
    dir1 = repository.get_director("Taika Waititi")
    dir2 = repository.get_director("Steven Speilberg")
    dir_dicts = services.directors_to_dict([dir2, dir1])
    assert dir_dicts[0]['name'] == "Steven Speilberg" and len(dir_dicts) == 2
    assert services.director_to_dict("not a director") is None


def test_actors_to_dict(repository):
    actor1 = repository.get_actor("Chris Pratt")
    actor2 = repository.get_actor("Emma Watson")
    actor_dicts = services.actors_to_dict([actor1, actor2])
    assert actor_dicts[0]['name'] == "Chris Pratt" and len(actor_dicts) == 2
    assert services.director_to_dict("not an actor") is None


def test_genres_to_dict(repository):
    genre_dicts = services.genres_to_dict(repository.get_genres())
    assert genre_dicts[0]['name'] == "Animation" and len(genre_dicts) == 2
    assert services.director_to_dict("not a genre") is None


def test_get_directors_by_name(repository):
    assert services.get_directors_by_name("tai", repository) == [{'name': "Taika Waititi"}]
    assert services.get_directors_by_name("xyz", repository) == []


def test_get_actors_by_name(repository):
    assert services.get_actors_by_name("chri", repository) == [{'name': "Chris Pratt"}]
    assert services.get_actors_by_name("xyz", repository) == []


def test_get_genres(repository):
    assert services.get_genres(repository) == [{'name': "Animation"}, {'name': "Comedy"}]


def test_get_colleagues(repository):
    assert services.get_colleagues("Emma Watson", repository) == [{'name': "Tom Hanks"}]
    assert services.get_colleagues("xyz", repository) is None
    assert services.get_colleagues("Chris Pratt", repository) == []
