import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from flix.domainmodel.genre import Genre
from flix.domainmodel.movie import Movie
from flix.domainmodel.review import Review
from flix.domainmodel.user import User

review_time = datetime.date(2020, 2, 28)


def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute(
        'INSERT INTO users (user_name, password, time_spent_watching_movies_minutes) '
        'VALUES (:username, :password, 0)',
        {'username': new_name, 'password': new_password}
    )
    row = empty_session.execute(
        'SELECT id from users where user_name = :username',
        {'username': new_name}
    ).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute(
            'INSERT INTO users (user_name, password, time_spent_watching_movies_minutes) '
            'VALUES (:username, :password, 0)',
            {'username': value[0], 'password': value[1]}
        )
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_director(empty_session):
    empty_session.execute(
        "INSERT INTO directors (name) VALUES ('Ron Clements')"
    )
    row = empty_session.execute(
        "SELECT id from directors where name = 'Ron Clements'"
    ).fetchone()
    return row[0]


def insert_movie(empty_session):
    director_key = insert_director(empty_session)
    description = "In Ancient Polynesia, when a terrible curse incurred by the Demigod Maui reaches an impetuous " \
                  "Chieftain's daughter's island, she answers the Ocean's call to seek out the Demigod to set " \
                  "things right."
    empty_session.execute(
        "INSERT INTO movies (title, release_year, description, director_id, runtime_minutes) "
        "VALUES ('Moana', 2016, :description, :director_id, 107)",
        {'description': description, 'director_id': director_key}
    )
    row = empty_session.execute('SELECT id from movies').fetchone()
    return row[0]


def insert_genres(empty_session):
    empty_session.execute(
        'INSERT INTO genres (name) VALUES ("Animation"), ("Comedy")'
    )
    rows = list(empty_session.execute(
        'SELECT id from genres'
    ))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_watchlist(empty_session):
    user_key = insert_user(empty_session)
    empty_session.execute(
        'INSERT INTO watchlists (user_id) VALUES (:user_id)',
        {'user_id': user_key}
    )
    row = empty_session.execute('SELECT id from watchlists').fetchone()
    return row[0]


def insert_actor_colleague_associations(empty_session, actor_id, colleague_ids):
    stmt = 'INSERT INTO actor_colleagues (actor_id, colleague_id) VALUES (:actor_id, :colleague_id)'
    for colleague_id in colleague_ids:
        empty_session.execute(stmt, {'actor_id': actor_id, 'colleague_id': colleague_id})


def insert_movie_actor_associations(empty_session, movie_id, actor_ids):
    stmt = 'INSERT INTO movie_actors (movie_id, actor_id) VALUES (:movie_id, :actor_id)'
    for actor_id in actor_ids:
        empty_session.execute(stmt, {'movie_id': movie_id, 'actor_id': actor_id})


def insert_movie_genre_associations(empty_session, movie_id, genre_ids):
    stmt = 'INSERT INTO movie_genres (movie_id, genre_id) VALUES (:movie_id, :genre_id)'
    for genre_id in genre_ids:
        empty_session.execute(stmt, {'movie_id': movie_id, 'genre_id': genre_id})


def insert_user_watched_movie_associations(empty_session, user_id, movie_ids):
    stmt = 'INSERT INTO user_watched_movies (user_id, movie_id) VALUES (:user_id, :movie_id)'
    for movie_id in movie_ids:
        empty_session.execute(stmt, {'user_id': user_id, 'genre_id': movie_id})


def insert_watchlist_movie_associations(empty_session, watchlist_id, movie_ids):
    stmt = 'INSERT INTO watchlist_movies (watchlist_id, movie_id) VALUES (:watchlist_id, :movie_id)'
    for movie_id in movie_ids:
        empty_session.execute(stmt, {'watchlist_id': watchlist_id, 'genre_id': movie_id})


def insert_reviewed_movie(empty_session):
    movie_key = insert_movie(empty_session)
    user_key = insert_user(empty_session)

    timestamp_1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    empty_session.execute(
        'INSERT INTO reviews (movie_id, review_text, rating, timestamp) VALUES '
        '(:movie_id, "Review 1", 9, :timestamp_1),'
        '(:movie_id, "Review 2", 10, :timestamp_2)',
        {'movie_id': movie_key, 'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2}
    )

    row = empty_session.execute('SELECT id from movies').fetchone()
    return row[0]


def make_movie():
    movie = Movie(
        "Moana",
        2016
    )
    movie.description = "In Ancient Polynesia, when a terrible curse incurred by the Demigod Maui reaches an " \
                        "impetuous Chieftain's daughter's island, she answers the Ocean's call to seek out the " \
                        "Demigod to set things right."
    movie.runtime_minutes = 107
    return movie


def make_user():
    user = User("Andrew", "111")
    return user


def make_genre():
    genre = Genre("Comedy")
    return genre


def test_loading_of_users(empty_session):
    users = list()
    users.append(("Andrew", "1234"))
    users.append(("Cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User("Andrew", "1234"),
        User("Cindy", "999")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("Andrew", "111")]


def test_saving_of_users_with_common_username(empty_session):
    insert_user(empty_session, ("Andrew", "1234"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("Andrew", "111")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_movie(empty_session):
    movie_key = insert_movie(empty_session)
    expected_movie = make_movie()
    fetched_movie = empty_session.query(Movie).one()

    assert expected_movie == fetched_movie
    assert movie_key == fetched_movie.id


def test_loading_of_movie_with_genres(empty_session):
    movie_key = insert_movie(empty_session)
    genre_keys = insert_genres(empty_session)
    insert_movie_genre_associations(empty_session, movie_key, genre_keys)

    movie = empty_session.query(Movie).get(movie_key)
    genres = [empty_session.query(Genre).get(key) for key in genre_keys]

    for genre in genres:
        assert genre in movie.genres


def test_loading_of_reviewed_movie(empty_session):
    movie_key = insert_reviewed_movie(empty_session)
    movie = empty_session.query(Movie).get(movie_key)

    rows = empty_session.query(Review).filter(Review._movie == movie).all()

    assert len(rows) == 2


def test_saving_of_review(empty_session):
    movie_key = insert_movie(empty_session)
    user_key = insert_user(empty_session, ("Andrew", "1234"))

    rows = empty_session.query(Movie).all()
    movie = rows[0]
    user = empty_session.query(User).filter(User._user_name == "Andrew").one()

    # Create a new Comment that is bidirectionally linked with the User and Article.
    review_text = "Some review text."
    review = Review(movie, review_text, 10)
    user.add_review(review)

    # Note: if the bidirectional links between the new Comment and the User and
    # Article objects hadn't been established in memory, they would exist following
    # committing the addition of the Comment to the database.
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, movie_id, review_text FROM reviews'))

    assert rows == [(user_key, movie_key, review_text)]


def test_saving_of_movie(empty_session):
    movie = make_movie()
    empty_session.add(movie)
    empty_session.commit()

    rows = list(empty_session.execute(
        'SELECT title, release_year, description, runtime_minutes FROM movies'
    ))
    assert rows == [("Moana", 2016,
                     "In Ancient Polynesia, when a terrible curse incurred by the Demigod Maui reaches an "
                     "impetuous Chieftain's daughter's island, she answers the Ocean's call to seek out the "
                     "Demigod to set things right.", 107
                     )]


def test_saving_movie_with_genres(empty_session):
    movie = make_movie()
    genre = make_genre()

    # Establish the bidirectional relationship between the Article and the Tag.
    movie.genres.append(genre)

    # Persist the Article (and Tag).
    # Note: it doesn't matter whether we add the Tag or the Article. They are connected
    # bidirectionally, so persisting either one will persist the other.
    empty_session.add(movie)
    empty_session.commit()

    # Test test_saving_of_article() checks for insertion into the articles table.
    rows = list(empty_session.execute('SELECT id FROM movies'))
    movie_key = rows[0][0]

    # Check that the tags table has a new record.
    rows = list(empty_session.execute('SELECT id, name FROM genres'))
    genre_key = rows[0][0]
    assert rows[0][1] == "Comedy"

    # Check that the article_tags table has a new record.
    rows = list(empty_session.execute('SELECT movie_id, genre_id from movie_genres'))
    movie_foreign_key = rows[0][0]
    genre_foreign_key = rows[0][1]

    assert movie_key == movie_foreign_key
    assert genre_key == genre_foreign_key


def test_save_reviewed_movie(empty_session):
    # Create Article User objects.
    movie = make_movie()

    # Create a new Comment that is bidirectionally linked with the User and Article.
    review_text = "Some review text."
    review = Review(movie, review_text, 10)

    # Save the new Article.
    empty_session.add(review)
    empty_session.commit()

    # Test test_saving_of_article() checks for insertion into the articles table.
    rows = list(empty_session.execute('SELECT id FROM movies'))
    movie_key = rows[0][0]

    # Check that the comments table has a new record that links to the articles and users
    # tables.
    rows = list(empty_session.execute('SELECT movie_id, review_text FROM reviews'))
    assert rows == [(movie_key, review_text)]
