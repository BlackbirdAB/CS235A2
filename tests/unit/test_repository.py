import pytest

from flix.adapters.memory_repository import MemoryRepository
from flix.domainmodel.actor import Actor
from flix.domainmodel.director import Director
from flix.domainmodel.genre import Genre
from flix.domainmodel.movie import Movie
from flix.domainmodel.review import Review
from flix.domainmodel.user import User


@pytest.fixture()
def repository():
    return MemoryRepository()


def test_add_and_get_director(repository):
    repository.add_director(Director("Taika Waititi"))
    assert repository.get_director("Taika Waititi") == Director("Taika Waititi")
    assert repository.get_director("Steven Speilberg") is None


def test_get_directors_by_name(repository):
    repository.add_director(Director("Taika Waititi"))
    repository.add_director(Director("Steven Speilberg"))
    assert repository.get_directors_by_name("taik") == [Director("Taika Waititi")]
    assert repository.get_directors_by_name("xyz") == []
    assert repository.get_directors_by_name("t") == [Director("Taika Waititi"), Director("Steven Speilberg")]
    assert repository.get_directors_by_name(1) == []


def test_add_and_get_actor(repository):
    repository.add_actor(Actor("Chris Pratt"))
    assert repository.get_actor("Chris Pratt") == Actor("Chris Pratt")
    assert repository.get_actor("Emma Watson") is None


def test_get_actors_by_name(repository):
    repository.add_actor(Actor("Chris Pratt"))
    repository.add_actor(Actor("Emma Watson"))
    assert repository.get_actors_by_name("chri") == [Actor("Chris Pratt")]
    assert repository.get_actors_by_name("xyz") == []
    assert repository.get_actors_by_name("t") == [Actor("Chris Pratt"), Actor("Emma Watson")]
    assert repository.get_actors_by_name(1) == []


def test_add_and_get_users(repository):
    assert repository.get_users() == []
    repository.add_user(User("Myles Kennedy", "123"))
    repository.add_user(User("Mark Tremonti", "456"))
    repository.add_user(User("Mark Tremonti", "456"))
    assert repository.get_user("Myles Kennedy") == User("Myles Kennedy", "123")
    assert repository.get_user("Scott Phillips") is None
    assert repository.get_users() == [User("Myles Kennedy", "123"), User("Mark Tremonti", "456")]


def test_add_and_get_movies(repository):
    assert repository.get_movies() == []
    repository.add_movie(Movie("Moana", 2016))
    repository.add_movie(Movie("Ice Age", 2002))
    repository.add_movie(Movie("Ice Age", 2002))
    assert repository.get_movie("Moana", 2016) == Movie("Moana", 2016)
    assert repository.get_movie("A Silent Voice", 2016) is None
    assert repository.get_movies() == [Movie("Ice Age", 2002), Movie("Moana", 2016)]


def test_get_movies_by_title(repository):
    repository.add_movie(Movie("Moana", 2016))
    repository.add_movie(Movie("Ice Age", 2002))
    assert repository.get_movies_by_title("moa") == [Movie("Moana", 2016)]
    assert repository.get_movies_by_title("xyz") == []
    assert repository.get_movies_by_title("a") == [Movie("Ice Age", 2002), Movie("Moana", 2016)]
    assert repository.get_movies_by_title(1) == []


def test_get_movies_by_director(repository):
    movie1 = Movie("Moana", 2016)
    movie1.director = Director("Taika Waititi")
    movie2 = Movie("Ice Age", 2002)
    movie2.director = Director("Steven Speilberg")
    movie3 = Movie("A Silent Voice", 2016)
    movie3.director = Director("Steven Speilberg")
    repository.add_movie(movie1)
    repository.add_movie(movie2)
    repository.add_movie(movie3)
    assert repository.get_movies_by_director("Taika Waititi") == [movie1]
    assert repository.get_movies_by_director("xyz") == []
    assert repository.get_movies_by_director("Steven Speilberg") == [movie3, movie2]
    assert repository.get_movies_by_director(1) == []


def test_get_movies_by_actor(repository):
    movie1 = Movie("Moana", 2016)
    movie1.add_actor(Actor("Chris Pratt"))
    movie1.add_actor(Actor("Emma Watson"))
    movie2 = Movie("Ice Age", 2002)
    movie2.add_actor(Actor("Emma Watson"))
    repository.add_movie(movie1)
    repository.add_movie(movie2)
    assert repository.get_movies_by_actor("Chris Pratt") == [movie1]
    assert repository.get_movies_by_actor("xyz") == []
    assert repository.get_movies_by_actor("Emma Watson") == [movie2, movie1]
    assert repository.get_movies_by_actor(1) == []


def test_get_movies_by_genre(repository):
    movie1 = Movie("Moana", 2016)
    movie1.add_genre(Genre("Comedy"))
    movie1.add_genre(Genre("Animated"))
    movie2 = Movie("Ice Age", 2002)
    movie2.add_genre(Genre("Animated"))
    repository.add_movie(movie1)
    repository.add_movie(movie2)
    assert repository.get_movies() == [movie2, movie1]
    assert repository.get_movies_by_genre("Comedy") == [movie1]
    assert repository.get_movies_by_genre("xyz") == []
    assert repository.get_movies_by_genre("Animated") == [movie2, movie1]
    assert repository.get_movies_by_genre(1) == []


def test_get_number_of_movies(repository):
    assert repository.get_number_of_movies() == 0
    repository.add_movie(Movie("Moana", 2016))
    assert repository.get_number_of_movies() == 1
    repository.add_movie(Movie("Ice Age", 2002))
    assert repository.get_number_of_movies() == 2


def test_add_and_get_genres(repository):
    repository.add_genre(Genre("Comedy"))
    repository.add_genre(Genre("Comedy"))
    repository.add_genre(Genre("Animated"))
    assert repository.get_genres() == [Genre("Animated"), Genre("Comedy")]


def test_add_and_get_reviews(repository):
    review1 = Review(Movie("Moana", 2016), "Very good", 8)
    review2 = Review(Movie("Ice Age", 2002), "Excellent", 10)
    repository.add_review(review1)
    repository.add_review(review2)
    assert repository.get_reviews() == [review1, review2]
