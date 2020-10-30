from typing import List
from flix.domainmodel.movie import Movie
from flix.domainmodel.review import Review
from flix.domainmodel.watchlist import WatchList


class User:
    def __init__(self, user_name, password):
        if user_name == "" or type(user_name) is not str:
            self._user_name = None
        else:
            self._user_name = user_name.strip()
        if password == "" or type(password) is not str:
            self._password = None
        else:
            self._password = password
        self._watched_movies: List[Movie] = list()
        self._reviews: List[Review] = list()
        self._time_spent_watching_movies_minutes: int = 0
        self._watchlist = WatchList()

    @property
    def user_name(self) -> str:
        return self._user_name

    @property
    def password(self) -> str:
        return self._password

    @property
    def watched_movies(self) -> List[Movie]:
        return self._watched_movies

    @property
    def reviews(self) -> List[Review]:
        return self._reviews

    @property
    def time_spent_watching_movies_minutes(self) -> int:
        return self._time_spent_watching_movies_minutes

    @property
    def watchlist(self):
        return self._watchlist

    def __repr__(self):
        return f"<User {self._user_name}>"

    def __eq__(self, other):
        if type(other) is not User:
            return False
        else:
            return self._user_name.lower() == other._user_name.lower()

    def __lt__(self, other):
        return self._user_name < other._user_name

    def __hash__(self):
        return hash(self._user_name)

    def watch_movie(self, movie):
        if type(movie) is Movie:
            if movie not in self._watched_movies:
                self._watched_movies.append(movie)
            self._time_spent_watching_movies_minutes += movie.runtime_minutes
            print(self._user_name, self._watched_movies, self._time_spent_watching_movies_minutes)

    def add_review(self, review):
        if type(review) is Review:
            self._reviews.append(review)
