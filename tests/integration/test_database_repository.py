import pytest

from flix.adapters.database_repository import SqlAlchemyRepository
from flix.domainmodel.actor import Actor
from flix.domainmodel.director import Director
from flix.domainmodel.genre import Genre
from flix.domainmodel.movie import Movie
from flix.domainmodel.review import Review
from flix.domainmodel.user import User
from flix.adapters.repository import RepositoryException


def test_add_and_get_director(session_factory):
    repository = SqlAlchemyRepository(session_factory)
    repository.add_director(Director("Mari Okada"))
    assert repository.get_director("Mari Okada").director_full_name == "Mari Okada"
    assert repository.get_director("Mari Omada") is None


def test_get_directors_by_name(session_factory):
    repository = SqlAlchemyRepository(session_factory)
    repository.add_director(Director("Mari Okada"))
    repository.add_director(Director("Mari Omada"))
    assert repository.get_directors_by_name("mari ok") == [Director("Mari Okada")]
    assert repository.get_directors_by_name("xyz") == []
    assert repository.get_directors_by_name("mari o") == [Director("Mari Okada"), Director("Mari Omada")]
    assert repository.get_directors_by_name(1) == []


def test_add_and_get_actor(session_factory):
    repository = SqlAlchemyRepository(session_factory)
    repository.add_actor(Actor("Ikue Ootani"))
    assert repository.get_actor("Ikue Ootani") == Actor("Ikue Ootani")
    assert repository.get_actor("Satomi Arai") is None


def test_get_actors_by_name(session_factory):
    repository = SqlAlchemyRepository(session_factory)
    repository.add_actor(Actor("Ikue Ootani"))
    repository.add_actor(Actor("Ikue Arai"))
    assert repository.get_actors_by_name("ikue ootani") == [Actor("Ikue Ootani")]
    assert repository.get_actors_by_name("xyz") == []
    assert repository.get_actors_by_name("ikue ") == [Actor("Ikue Arai"), Actor("Ikue Ootani")]
    assert repository.get_actors_by_name(1) == []


def test_add_and_get_users(session_factory):
    repository = SqlAlchemyRepository(session_factory)
    assert repository.get_users() == []
    repository.add_user(User("Brian Marshall", "123"))
    repository.add_user(User("Mark Tremonti", "456"))
    repository.add_user(User("Mark Tremonti", "456"))
    assert repository.get_user("Brian Marshall") == User("Brian Marshall", "123")
    assert repository.get_user("Scott Phillips") is None
    assert repository.get_users() == [User("Brian Marshall", "123"), User("Mark Tremonti", "456")]


def test_add_and_get_movies(session_factory):
    repository = SqlAlchemyRepository(session_factory)
    maquia = Movie("Maquia", 2018)
    iceage = Movie("Ice Age", 2002)
    maquia.description = "The Iorph people live far away from the world of humans, spending their days weaving " \
                         "Hibiol, a special cloth serving as a written chronicle every time. They age more slowly " \
                         "than humans and have the capacity to live for hundreds of years."
    maquia.runtime_minutes = 115
    iceage.description = "A Cronopio known as Scrat attempts to find a place to store his acorn for the winter. " \
                         "Eventually, as he tries to stomp it into the ground, he inadvertently causes a large " \
                         "crack to form in the ice that extends for miles before setting off a large avalanche " \
                         "which nearly crushes him."
    iceage.runtime_minutes = 81
    repository.add_movie(maquia)
    repository.add_movie(iceage)
    repository.add_movie(iceage)
    assert repository.get_movie("Maquia", 2018) == Movie("Maquia", 2018)
    assert repository.get_movie("A Silent Voice", 2016) is None
    movies = repository.get_movies()
    assert Movie("Ice Age", 2002) in movies and Movie("Maquia", 2018) in movies


def test_get_movies_by_title(session_factory):
    repository = SqlAlchemyRepository(session_factory)
    assert repository.get_movies_by_title("moana") == [Movie("Moana", 2016)]
    assert repository.get_movies_by_title("xyz") == []
    assert repository.get_movies_by_title("avengers") == [Movie("Avengers: Age of Ultron", 2015), Movie("The Avengers", 2012)]
    assert repository.get_movies_by_title(1) == []


def test_get_movies_by_director(session_factory):
    repository = SqlAlchemyRepository(session_factory)

    assert repository.get_movies_by_director("Taika Waititi") == [Movie("Hunt for the Wilderpeople", 2016)]
    assert repository.get_movies_by_director("xyz") == []
    assert repository.get_movies_by_director("John Crowley") == [Movie("Brooklyn", 2015), Movie("Closed Circuit", 2013)]
    assert repository.get_movies_by_director(1) == []


def test_get_movies_by_actor(session_factory):
    repository = SqlAlchemyRepository(session_factory)
    assert repository.get_movies_by_actor("Taika Waititi") == [Movie("What We Do in the Shadows", 2014)]
    assert repository.get_movies_by_actor("xyz") == []
    assert repository.get_movies_by_actor("Isabelle Huppert") == [Movie("Elle", 2016), Movie("L'avenir", 2016)]
    assert repository.get_movies_by_actor(1) == []


def test_get_movies_by_genre(session_factory):
    repository = SqlAlchemyRepository(session_factory)
    movie1 = Movie("Maquia", 2018)
    movie2 = Movie("Ice Age", 2002)
    genre1 = Genre("Japanese Anime")
    genre2 = Genre("Emotional")
    repository.add_genre(genre1)
    repository.add_genre(genre2)
    movie1.description = "The Iorph people live far away from the world of humans, spending their days weaving " \
                         "Hibiol, a special cloth serving as a written chronicle every time. They age more slowly " \
                         "than humans and have the capacity to live for hundreds of years."
    movie1.runtime_minutes = 115
    movie2.description = "A Cronopio known as Scrat attempts to find a place to store his acorn for the winter. " \
                         "Eventually, as he tries to stomp it into the ground, he inadvertently causes a large " \
                         "crack to form in the ice that extends for miles before setting off a large avalanche " \
                         "which nearly crushes him."
    movie2.runtime_minutes = 81
    movie1.add_genre(genre1)
    movie1.add_genre(genre2)
    movie2.add_genre(genre2)
    repository.add_movie(movie1)
    repository.add_movie(movie2)
    assert repository.get_movies_by_genre("Japanese Anime") == [movie1]
    assert repository.get_movies_by_genre("xyz") == []
    assert repository.get_movies_by_genre("Emotional") == [movie2, movie1]
    assert repository.get_movies_by_genre(1) == []


def test_get_number_of_movies(session_factory):
    repository = SqlAlchemyRepository(session_factory)
    initial_length = repository.get_number_of_movies()
    movie1 = Movie("Maquia", 2018)
    movie2 = Movie("Ice Age", 2002)
    movie1.description = "The Iorph people live far away from the world of humans, spending their days weaving " \
                         "Hibiol, a special cloth serving as a written chronicle every time. They age more slowly " \
                         "than humans and have the capacity to live for hundreds of years."
    movie1.runtime_minutes = 115
    movie2.description = "A Cronopio known as Scrat attempts to find a place to store his acorn for the winter. " \
                         "Eventually, as he tries to stomp it into the ground, he inadvertently causes a large " \
                         "crack to form in the ice that extends for miles before setting off a large avalanche " \
                         "which nearly crushes him."
    movie2.runtime_minutes = 81
    repository.add_movie(movie1)
    assert repository.get_number_of_movies() == initial_length + 1
    repository.add_movie(movie2)
    assert repository.get_number_of_movies() == initial_length + 2


def test_add_and_get_genres(session_factory):
    repository = SqlAlchemyRepository(session_factory)
    repository.add_genre(Genre("Japanese Anime"))
    repository.add_genre(Genre("Japanese Anime"))
    repository.add_genre(Genre("Emotional"))
    genres = repository.get_genres()
    assert Genre("Emotional") in genres and Genre("Japanese Anime") in genres


def test_add_and_get_reviews(session_factory):
    repository = SqlAlchemyRepository(session_factory)
    movie1 = repository.get_movie("Moana", 2016)
    movie2 = repository.get_movie("Inception", 2010)
    review1 = Review(movie1, "Very good", 8)
    review2 = Review(movie2, "Excellent", 10)
    repository.add_review(review1)
    repository.add_review(review2)
    assert repository.get_reviews() == [review1, review2]
