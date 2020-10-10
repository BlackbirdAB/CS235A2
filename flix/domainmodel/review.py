from datetime import datetime
from flix.domainmodel.movie import Movie


class Review:
    def __init__(self, movie, review_text, rating):
        self.__movie: Movie = movie
        self.__review_text: str = review_text
        if type(rating) is not int or rating > 10 or rating < 0:
            self.__rating = None
        else:
            self.__rating = rating
        self.__timestamp = datetime.today()

    @property
    def movie(self) -> Movie:
        return self.__movie

    @property
    def review_text(self) -> str:
        return self.__review_text

    @property
    def rating(self) -> int:
        return self.__rating

    @property
    def timestamp(self):
        return self.__timestamp

    def __repr__(self):
        return f"<Review {self.__movie.title}, {self.__timestamp}>"

    def __eq__(self, other):
        if type(other) is not Review:
            return False
        return self.__movie == other.__movie and self.__review_text == other.__review_text and \
            self.__rating == other.__rating and self.__timestamp == other.__timestamp
