from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.html5 import SearchField

import flix.adapters.repository as repo
import flix.utilities.services as services

from flix.domainmodel.movie import Movie


# Configure Blueprint.

utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_selected_movies(quantity=6):
    movies = services.get_random_movies(quantity, repo.repo_instance)

    return movies


def get_watchlist_empty():
    return services.get_watchlist_empty(repo.repo_instance)


def get_user(username: str):
    return services.get_user(username, repo.repo_instance)


def movie_to_dict(movie: Movie):
    return services.movie_to_dict(movie)


class SearchForm(FlaskForm):
    search_term = SearchField('Search')
    submit = SubmitField('Search')