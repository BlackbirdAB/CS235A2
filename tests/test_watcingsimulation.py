import pytest
from flix.domainmodel.movie import Movie
from activitysimulations.watchingsimulation import MovieWatchingSimulation
from flix.domainmodel.user import User


@pytest.fixture()
def simulation():
    return MovieWatchingSimulation(Movie("Moana", 2016))


def test_constructor(simulation):
    assert simulation.movie == Movie("Moana", 2016)
    sim2 = MovieWatchingSimulation(42)
    assert sim2.movie is None


def test_movie_setter(simulation):
    simulation.movie = Movie("Ice Age", 2002)
    assert simulation.movie == Movie("Ice Age", 2002)
    simulation.movie = 42
    assert simulation.movie == Movie("Ice Age", 2002)


def test_add_user(simulation):
    simulation.add_user(User("Myles Kennedy", "abcde"))
    assert len(simulation.users) == 1
    assert simulation.users[0] == User("Myles Kennedy", "abcde")


def test_add_duplicate_user(simulation):
    simulation.add_user(User("Myles Kennedy", "abcde"))
    simulation.add_user(User("Myles Kennedy", "abcde"))
    assert len(simulation.users) == 1
    assert simulation.users == [User("Myles Kennedy", "abcde")]


def test_remove_user(simulation):
    simulation.add_user(User("Myles Kennedy", "abcde"))
    simulation.remove_user(User("Myles Kennedy", "abcde"))
    assert len(simulation.users) == 0
    assert simulation.users == []


def test_remove_non_existent_user(simulation):
    simulation.add_user(User("Myles Kennedy", "abcde"))
    simulation.remove_user(User("Mark Tremonti", "fghij"))
    assert len(simulation.users) == 1
    assert simulation.users == [User("Myles Kennedy", "abcde")]


def test_write_review(simulation):
    user1 = User("Myles Kennedy", "abcde")
    simulation.add_user(user1)
    simulation.write_review(user1, "Great movie", 7)
    assert user1.reviews[0].movie == Movie("Moana", 2016)
    assert user1.reviews[0].review_text == "Great movie"
    assert user1.reviews[0].rating == 7


def test_write_review_by_user_not_in_sim(simulation):
    user1 = User("Myles Kennedy", "abcde")
    simulation.write_review(user1, "Great movie", 7)
    assert len(user1.reviews) == 0


def test_write_review_with_rating_out_of_range(simulation):
    user1 = User("Myles Kennedy", "abcde")
    simulation.add_user(user1)
    simulation.write_review(user1, "Great movie", 15)
    assert len(user1.reviews) == 0


def test_write_review_with_no_movie(simulation):
    sim2 = MovieWatchingSimulation(42)
    assert sim2.movie is None
    user1 = User("Myles Kennedy", "abcde")
    sim2.add_user(user1)
    sim2.write_review(user1, "Great movie", 7)
    assert len(user1.reviews) == 0


def test_start_watching(simulation):
    simulation.movie.runtime_minutes = 10
    user1 = User("Myles Kennedy", "abcde")
    user2 = User("Mark Tremonti", "fghij")
    simulation.add_user(user1)
    simulation.add_user(user2)
    assert simulation.movie not in user1.watched_movies
    assert user1.time_spent_watching_movies_minutes == 0
    assert simulation.movie not in user2.watched_movies
    assert user2.time_spent_watching_movies_minutes == 0
    simulation.start_watching()
    assert simulation.movie in user1.watched_movies
    assert user1.time_spent_watching_movies_minutes == 10
    assert simulation.movie in user2.watched_movies
    assert user2.time_spent_watching_movies_minutes == 10


def test_start_watching_with_no_movie(simulation):
    sim2 = MovieWatchingSimulation(42)
    assert sim2.movie is None
    user1 = User("Myles Kennedy", "abcde")
    user2 = User("Mark Tremonti", "fghij")
    sim2.add_user(user1)
    sim2.add_user(user2)
    assert len(user1.watched_movies) == 0
    assert user1.time_spent_watching_movies_minutes == 0
    assert len(user2.watched_movies) == 0
    assert user2.time_spent_watching_movies_minutes == 0
    sim2.start_watching()
    assert len(user1.watched_movies) == 0
    assert user1.time_spent_watching_movies_minutes == 0
    assert len(user2.watched_movies) == 0
    assert user2.time_spent_watching_movies_minutes == 0
