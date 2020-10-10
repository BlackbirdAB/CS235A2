from flask import Blueprint, render_template, url_for

import flix.utilities.utilities as utilities

home_blueprint = Blueprint('home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    movies = utilities.get_selected_movies()
    for list_movie in movies:
        list_movie['url'] = url_for('movies_bp.movie', title=list_movie['title'],
                                    release_year=list_movie['release_year'])
        list_movie['review_url'] = url_for('movies_bp.review_movie', title=list_movie['title'],
                                           release_year=list_movie['release_year'])
    return render_template(
        'home/home.html',
        selected_movies=movies,
        watchlist_empty=utilities.get_watchlist_empty()
    )
