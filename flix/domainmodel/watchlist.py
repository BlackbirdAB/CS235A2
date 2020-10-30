from typing import List

from flix.domainmodel.movie import Movie


class WatchList:
    def __init__(self):
        self._watch_list: List[Movie] = list()

    def __repr__(self):
        return repr(self._watch_list)

    def __iter__(self):
        self.index = -1
        return self

    def __next__(self):
        if self.index < len(self._watch_list) - 1:
            self.index += 1
            return self._watch_list[self.index]
        else:
            raise StopIteration

    def add_movie(self, movie):
        if type(movie) is Movie and movie not in self._watch_list:
            self._watch_list.append(movie)

    def remove_movie(self, movie):
        if type(movie) is Movie and movie in self._watch_list:
            self._watch_list.remove(movie)

    def select_movie_to_watch(self, index):
        if type(index) is int:
            if 0 <= index < len(self._watch_list):
                return self._watch_list[index]
            else:
                return None

    def size(self):
        return len(self._watch_list)

    def first_movie_in_watchlist(self):
        if len(self._watch_list) > 0:
            return self._watch_list[0]
        else:
            return None
