from typing import List

from flix.domainmodel.movie import Movie
from flix.domainmodel.user import User
from flix.domainmodel.review import Review


class MovieWatchingSimulation:
    def __init__(self, movie: Movie):
        if type(movie) is Movie:
            self.__movie = movie
        else:
            self.__movie = None
        self.__users: List[User] = list()

    @property
    def movie(self):
        return self.__movie

    @property
    def users(self):
        return self.__users

    @movie.setter
    def movie(self, new_movie):
        if type(new_movie) is Movie:
            self.__movie = new_movie

    def add_user(self, user):
        if type(user) is User and user not in self.__users:
            self.__users.append(user)

    def remove_user(self, user):
        if type(user) is User and user in self.__users:
            self.__users.remove(user)

    def write_review(self, user, review_text, rating):
        if type(user) is User and user in self.__users and type(review_text) is str and type(rating) is int \
                and 11 > rating >= 0 and self.__movie is not None:
            review = Review(self.__movie, review_text, rating)
            user.add_review(review)

    def start_watching(self):
        if len(self.__users) > 0 and self.__movie is not None:
            for user in self.__users:
                user.watch_movie(self.__movie)
