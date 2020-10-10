import pytest

from flask import session


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid username and password.
    response = client.post(
        '/authentication/register',
        data={'username': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Your username is required'),
        ('cj', '', b'Your username is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter, '
                         b'a lower case letter and a digit'),
        ('Myles Kennedy', '123ABcdefg', b'Your username is already taken - please supply another'),
))
def test_register_with_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['username'] == 'myles kennedy'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'Land of 1000 Movies' in response.data


def test_movies_by_title_without_title(client):
    # Check that we can retrieve the articles page.
    response = client.get('/movies_by_title')
    assert response.status_code == 200

    # Check that without providing a date query parameter the page includes the first article.
    assert b'Search Results For:' not in response.data


def test_movies_by_title_with_title(client):
    # Check that we can retrieve the articles page.
    response = client.get('/movies_by_title?title=inception')
    assert response.status_code == 200

    # Check that all articles on the requested date are included on the page.
    assert b'Search Results For:' in response.data
    assert b'Inception (2010)' in response.data
    assert b'A thief, who steals corporate secrets through use of dream-sharing technology, ' \
           b'is given the inverse task of planting an idea into the mind of a CEO.' in response.data


def test_movies_by_director_without_director(client):
    # Check that we can retrieve the articles page.
    response = client.get('/movies_by_director')
    assert response.status_code == 200

    # Check that without providing a date query parameter the page includes the first article.
    assert b'Search Results For:' not in response.data


def test_movies_by_director_with_director(client):
    # Check that we can retrieve the articles page.
    response = client.get('/movies_by_director?director=Christopher+Nolan')
    assert response.status_code == 200

    # Check that all articles on the requested date are included on the page.
    assert b'Search Results For:' in response.data
    assert b'Inception (2010)' in response.data
    assert b'A thief, who steals corporate secrets through use of dream-sharing technology, ' \
           b'is given the inverse task of planting an idea into the mind of a CEO.' in response.data
    assert b'The Dark Knight Rises (2012)' in response.data


def test_movies_by_actor_without_actor(client):
    # Check that we can retrieve the articles page.
    response = client.get('/movies_by_actor')
    assert response.status_code == 200

    # Check that without providing a date query parameter the page includes the first article.
    assert b'Search Results For:' not in response.data


def test_movies_by_actor_with_actor(client):
    # Check that we can retrieve the articles page.
    response = client.get('/movies_by_actor?actor=Leonardo+DiCaprio')
    assert response.status_code == 200

    # Check that all articles on the requested date are included on the page.
    assert b'Search Results For:' in response.data
    assert b'Inception (2010)' in response.data
    assert b'A thief, who steals corporate secrets through use of dream-sharing technology, ' \
           b'is given the inverse task of planting an idea into the mind of a CEO.' in response.data
    assert b'Blood Diamond (2006)' in response.data


def test_movies_by_genre_without_genre(client):
    # Check that we can retrieve the articles page.
    response = client.get('/movies_by_genre')
    assert response.status_code == 200

    # Check that without providing a date query parameter the page includes the first article.
    assert b'Search Results For:' not in response.data


def test_movies_by_genre_with_genre(client):
    # Check that we can retrieve the articles page.
    response = client.get('/movies_by_genre?genre=Action')
    assert response.status_code == 200

    # Check that all articles on the requested date are included on the page.
    assert b'Search Results For:' in response.data
    assert b'13 Hours (2016)' in response.data
    assert b'During an attack on a U.S. compound in Libya, a security team struggles to make sense out of the chaos.' \
           in response.data
    assert b'22 Jump Street (2014)' in response.data


def test_login_required_to_review(client):
    response = client.post('/review')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_review(client, auth):
    auth.login()

    response = client.get('/review?title=Inception&release_year=2010')

    response = client.post(
        '/review',
        data={'review': 'Amazing movie', 'rating': 10, 'movie_title': 'Inception', 'release_year': 2010}
    )
    assert response.headers['Location'] == 'http://localhost/reviews?title=Inception&release_year=2010'


@pytest.mark.parametrize(('review', 'rating', 'messages'), (
        ('Fucking horrible', 0, b'Your review must not contain profanity'),
        ('ok', 5, b'Your review is too short'),
        ('Its alright I guess', 15, b'Please choose a rating from 0 to 10'),
        ('ass', 11, (b'Your review is too short', b'Your review must not contain profanity',
                     b'Please choose a rating from 0 to 10')),
))
def test_review_with_invalid_input(client, auth, review, rating, messages):
    # Login a user.
    auth.login()

    # Attempt to comment on an article.
    response = client.post(
        '/review',
        data={'review': review, 'rating': rating, 'movie_title': 'Inception', 'release_year': 2010}
    )
    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response.data


def test_movie_without_valid_parameters(client):
    response = client.get('/movie')
    assert response.headers['Location'] == 'http://localhost/'


def test_movie_with_valid_parameters(client):
    response = client.get('/movie?title=Inception&release_year=2010')
    assert response.status_code == 200

    assert b'Inception (2010)' in response.data
    assert b'A thief, who steals corporate secrets through use of dream-sharing technology, ' \
           b'is given the inverse task of planting an idea into the mind of a CEO.' in response.data
    assert b'Directed by Christopher Nolan' in response.data
    assert b'Leonardo DiCaprio' in response.data
    assert b'Action' in response.data
    assert b'Runtime: 148 minutes' in response.data


def test_movie_in_watchlist(client):
    response = client.get('/movie?title=The+Da+Vinci+Code&release_year=2006')
    assert response.status_code == 200

    assert b'The Da Vinci Code (2006)' in response.data


def test_get_reviews_with_no_movie(client):
    response = client.get('/reviews')
    assert response.headers['Location'] == 'http://localhost/'


def test_get_reviews_for_movie(client):
    response = client.get('/reviews?title=Inception&release_year=2010')
    assert response.status_code == 200

    assert b'Reviews for Inception (2010)' in response.data
    assert b'Absolutely incredible movie!' in response.data


def test_login_required_to_view_watchlist(client):
    response = client.get('/watchlist')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_watchlist(client, auth):
    auth.login()

    response = client.get('/watchlist')

    assert response.status_code == 200

    assert b'The Da Vinci Code (2006)' in response.data
    assert b'Moana (2016)' in response.data


def test_search_for_director_without_director(client):
    response = client.get('/search_for_director')
    assert response.status_code == 200

    assert b'Search Results For:' not in response.data


def test_search_for_director_with_director(client):
    response = client.get('/search_for_director?director=christopher')
    assert response.status_code == 200

    assert b'Search Results For:' in response.data
    assert b'Christopher Landon' in response.data
    assert b'Christopher Nolan' in response.data


def test_search_for_actor_without_actor(client):
    response = client.get('/search_for_actor')
    assert response.status_code == 200

    assert b'Search Results For:' not in response.data


def test_search_for_actor_with_actor(client):
    response = client.get('/search_for_actor?actor=leo')
    assert response.status_code == 200

    assert b'Search Results For:' in response.data
    assert b'Edoardo Leo' in response.data
    assert b'Leonardo DiCaprio' in response.data
    assert b'Colleagues' in response.data


def test_search_for_genre(client):
    response = client.get('/search_for_genre')
    assert response.status_code == 200

    assert b'Search by Genre:' in response.data
    assert b'Action' in response.data
    assert b'Family' in response.data
