from datetime import datetime
from flix.domainmodel.movie import Movie


class Review:
    def __init__(self, movie, review_text, rating):
        self._movie: Movie = movie
        self._review_text: str = review_text
        if type(rating) is not int or rating > 10 or rating < 0:
            self._rating = None
        else:
            self._rating = rating
        self._timestamp = datetime.today()

    @property
    def movie(self) -> Movie:
        return self._movie

    @property
    def review_text(self) -> str:
        return self._review_text

    @property
    def rating(self) -> int:
        return self._rating

    @property
    def timestamp(self):
        return self._timestamp

    def __repr__(self):
        return f"<Review {self._movie.title}, {self._timestamp}>"

    def __eq__(self, other):
        if type(other) is not Review:
            return False
        return self._movie == other._movie and self._review_text == other._review_text and \
            self._rating == other._rating and self._timestamp == other._timestamp
