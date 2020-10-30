class Genre:
    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self._genre_name = None
        else:
            self._genre_name = genre_name.strip()

    @property
    def genre_name(self) -> str:
        return self._genre_name

    def __repr__(self):
        return f"<Genre {self._genre_name}>"

    def __eq__(self, other):
        if not isinstance(other, Genre):
            return False
        else:
            return other._genre_name == self._genre_name

    def __lt__(self, other):
        return self._genre_name < other._genre_name

    def __hash__(self):
        return hash(self._genre_name)


class TestGenreMethods:
    def test_init(self):
        genre1 = Genre("Horror")
        assert repr(genre1) == "<Genre Horror>"
        genre2 = Genre("")
        assert genre2.genre_name is None
