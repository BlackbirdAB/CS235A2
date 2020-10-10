from collections import Iterable

import pytest

from flix.domainmodel.movie import Movie
from flix.domainmodel.watchlist import WatchList


@pytest.fixture()
def watchlist():
    return WatchList()


def test_repr(watchlist):
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    assert repr(watchlist) == "[<Movie Moana, 2016>, <Movie Ice Age, 2002>]"


def test_iteration(watchlist):
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    assert isinstance(watchlist, Iterable)


def test_add_movie(watchlist):
    watchlist.add_movie(Movie("Moana", 2016))
    assert repr(watchlist) == "[<Movie Moana, 2016>]"


def test_add_duplicate_movie(watchlist):
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Moana", 2016))
    assert repr(watchlist) == "[<Movie Moana, 2016>]"


def test_remove_movie(watchlist):
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.remove_movie(Movie("Moana", 2016))
    assert repr(watchlist) == "[]"


def test_remove_non_existent_movie(watchlist):
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist.remove_movie(Movie("Moana", 2016))
    assert repr(watchlist) == "[<Movie Ice Age, 2002>]"


def test_size(watchlist):
    assert watchlist.size() == 0
    watchlist.add_movie(Movie("Moana", 2016))
    assert watchlist.size() == 1
    watchlist.add_movie(Movie("Ice Age", 2002))
    assert watchlist.size() == 2
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
    assert watchlist.size() == 3


def test_select_movie_to_watch_success(watchlist):
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
    assert watchlist.select_movie_to_watch(1) == Movie("Ice Age", 2002)


def test_select_movie_to_watch_failure(watchlist):
    watchlist.add_movie(Movie("Moana", 2016))
    assert watchlist.select_movie_to_watch(1) is None


def test_first_movie_in_watchlist_success(watchlist):
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    assert watchlist.first_movie_in_watchlist() == Movie("Moana", 2016)


def test_first_movie_in_watchlist_failure(watchlist):
    assert watchlist.first_movie_in_watchlist() is None
