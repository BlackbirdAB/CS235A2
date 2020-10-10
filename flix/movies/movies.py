from better_profanity import profanity
from flask import Blueprint, request, redirect, url_for, render_template, session
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

from flix.adapters import repository as repo
import flix.movies.services as services
from flix.authentication.authentication import login_required
import flix.utilities.utilities as utilities

movies_blueprint = Blueprint('movies_bp', __name__)


@movies_blueprint.route('/movies_by_title', methods=['GET', 'POST'])
def movies_by_title():
    target_title = None
    search_form = utilities.SearchForm()
    search_form.search_term.label = "Search by Title"
    if search_form.validate_on_submit():
        target_title = search_form.search_term.data
        return redirect(url_for('movies_bp.movies_by_title', title=target_title))

    if request.method == 'GET':
        target_title = request.args.get('title')

    movies = []
    title = ""
    if target_title is not None and len(target_title.strip()) > 0:
        movies = services.get_movies_by_title(target_title, repo.repo_instance)
        for list_movie in movies:
            list_movie['url'] = url_for('movies_bp.movie', title=list_movie['title'],
                                        release_year=list_movie['release_year'])
            list_movie['review_url'] = url_for('movies_bp.review_movie', title=list_movie['title'],
                                               release_year=list_movie['release_year'])
        title += 'Search Results For: "' + target_title + '"'

    movies_id = 0
    if request.args.get('next_id') is not None:
        movies_id = int(request.args.get('next_id'))
    next_id = min(movies_id + 6, len(movies))
    prev_id = max(movies_id - 6, 0)
    next_movies = False
    prev_movies = False
    if len(movies) - (movies_id + 1) >= 6:
        next_movies = True
    if movies_id >= 6:
        prev_movies = True

    return render_template(
        'search/movies_list_w_search.html',
        title=title,
        movies=movies[movies_id: next_id],
        prev_movies=prev_movies,
        prev_movies_url=url_for('movies_bp.movies_by_title', title=target_title, next_id=prev_id),
        next_movies=next_movies,
        next_movies_url=url_for('movies_bp.movies_by_title', title=target_title, next_id=next_id),
        handler_url=url_for('movies_bp.movies_by_title', title=target_title),
        search_form=search_form,
        watchlist_empty=utilities.get_watchlist_empty()
    )


@movies_blueprint.route('/movies_by_director', methods=['GET', 'POST'])
def movies_by_director():
    target_director = None
    search_form = utilities.SearchForm()
    search_form.search_term.label = "Search by Director"
    if search_form.validate_on_submit():
        target_director = search_form.search_term.data
        return redirect(url_for('search_bp.search_for_director', director=target_director))

    if request.method == 'GET':
        target_director = request.args.get('director')

    movies = []
    title = ""
    if target_director is not None and len(target_director.strip()) > 0:
        movies = services.get_movies_by_director(target_director, repo.repo_instance)
        for list_movie in movies:
            list_movie['url'] = url_for('movies_bp.movie', title=list_movie['title'],
                                        release_year=list_movie['release_year'])
            list_movie['review_url'] = url_for('movies_bp.review_movie', title=list_movie['title'],
                                               release_year=list_movie['release_year'])
        title += 'Search Results For: "' + target_director + '"'

    movies_id = 0
    if request.args.get('next_id') is not None:
        movies_id = int(request.args.get('next_id'))
    next_id = min(movies_id + 6, len(movies))
    prev_id = max(movies_id - 6, 0)
    next_movies = False
    prev_movies = False
    if len(movies) - (movies_id + 1) >= 6:
        next_movies = True
    if movies_id >= 6:
        prev_movies = True

    return render_template(
        'search/movies_list_w_search.html',
        title=title,
        movies=movies[movies_id: next_id],
        prev_movies=prev_movies,
        prev_movies_url=url_for('movies_bp.movies_by_director', director=target_director, next_id=prev_id),
        next_movies=next_movies,
        next_movies_url=url_for('movies_bp.movies_by_director', director=target_director, next_id=next_id),
        handler_url=url_for('movies_bp.movies_by_director', director=target_director),
        search_form=search_form,
        watchlist_empty=utilities.get_watchlist_empty()
    )


@movies_blueprint.route('/movies_by_actor', methods=['GET', 'POST'])
def movies_by_actor():
    target_actor = None
    search_form = utilities.SearchForm()
    search_form.search_term.label = "Search by Actor"
    if search_form.validate_on_submit():
        target_actor = search_form.search_term.data
        return redirect(url_for('search_bp.search_for_actor', actor=target_actor))

    if request.method == 'GET':
        target_actor = request.args.get('actor')

    movies = []
    title = ""
    if target_actor is not None and len(target_actor.strip()) > 0:
        movies = services.get_movies_by_actor(target_actor, repo.repo_instance)
        for list_movie in movies:
            list_movie['url'] = url_for('movies_bp.movie', title=list_movie['title'],
                                        release_year=list_movie['release_year'])
            list_movie['review_url'] = url_for('movies_bp.review_movie', title=list_movie['title'],
                                               release_year=list_movie['release_year'])
        title += 'Search Results For: "' + target_actor + '"'

    movies_id = 0
    if request.args.get('next_id') is not None:
        movies_id = int(request.args.get('next_id'))
    next_id = min(movies_id + 6, len(movies))
    prev_id = max(movies_id - 6, 0)
    next_movies = False
    prev_movies = False
    if len(movies) - (movies_id + 1) >= 6:
        next_movies = True
    if movies_id >= 6:
        prev_movies = True

    return render_template(
        'search/movies_list_w_search.html',
        title=title,
        movies=movies[movies_id: next_id],
        prev_movies=prev_movies,
        prev_movies_url=url_for('movies_bp.movies_by_actor', actor=target_actor, next_id=prev_id),
        next_movies=next_movies,
        next_movies_url=url_for('movies_bp.movies_by_actor', actor=target_actor, next_id=next_id),
        handler_url=url_for('movies_bp.movies_by_actor', actor=target_actor),
        search_form=search_form,
        watchlist_empty=utilities.get_watchlist_empty()
    )


@movies_blueprint.route('/movies_by_genre', methods=['GET', 'POST'])
def movies_by_genre():
    target_genre = request.args.get('genre')
    movies = []
    title = ""
    if target_genre is not None and len(target_genre.strip()) > 0:
        movies = services.get_movies_by_genre(target_genre, repo.repo_instance)
        for list_movie in movies:
            list_movie['url'] = url_for('movies_bp.movie', title=list_movie['title'],
                                        release_year=list_movie['release_year'])
            list_movie['review_url'] = url_for('movies_bp.review_movie', title=list_movie['title'],
                                               release_year=list_movie['release_year'])
        title += 'Search Results For: "' + target_genre + '"'

    movies_id = 0
    if request.args.get('next_id') is not None:
        movies_id = int(request.args.get('next_id'))
    next_id = min(movies_id + 6, len(movies))
    prev_id = max(movies_id - 6, 0)
    next_movies = False
    prev_movies = False
    if len(movies) - (movies_id + 1) >= 6:
        next_movies = True
    if movies_id >= 6:
        prev_movies = True

    return render_template(
        'movies/movie_list.html',
        title=title,
        movies=movies[movies_id: next_id],
        prev_movies=prev_movies,
        prev_movies_url=url_for('movies_bp.movies_by_genre', genre=target_genre, next_id=prev_id),
        next_movies=next_movies,
        next_movies_url=url_for('movies_bp.movies_by_genre', genre=target_genre, next_id=next_id),
        watchlist_empty=utilities.get_watchlist_empty()
    )


@movies_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_movie():
    username = session['username']
    form = ReviewForm()

    if form.validate_on_submit():
        try:
            movie_title = form.movie_title.data
            release_year = int(form.release_year.data)
            print("movies: ", type(username))
            services.add_review(movie_title,
                                release_year,
                                username,
                                form.review.data,
                                int(form.rating.data),
                                repo.repo_instance)
            return redirect(url_for('movies_bp.reviews', title=movie_title, release_year=release_year))

        except services.UnknownUserException:
            return redirect(url_for('authentication_bp.login'))

    if request.method == 'GET':
        movie_title = request.args.get('title')
        release_year = int(request.args.get('release_year'))
        form.movie_title.data = movie_title
        form.release_year.data = release_year
    else:
        movie_title = form.movie_title.data
        release_year = int(form.release_year.data)

    reviewed_movie = services.get_movie(movie_title, release_year, repo.repo_instance)

    return render_template(
        'movies/review_movie.html',
        movie=services.movie_to_dict(reviewed_movie),
        handler_url=url_for('movies_bp.review_movie', title=movie_title, release_year=release_year),
        form=form,
        watchlist_empty=utilities.get_watchlist_empty()
    )


@movies_blueprint.route('/movie', methods=['GET'])
def movie():
    target_title = request.args.get('title')
    target_year = request.args.get('release_year')
    if target_year is not None:
        target_year = int(target_year)
    target_movie = services.get_movie(target_title, target_year, repo.repo_instance)
    if target_movie is None:
        return redirect(url_for('home_bp.home'))

    in_watchlist = False
    if 'username' in session:
        username = session['username']
        try:
            user = services.get_user(username, repo.repo_instance)
            if target_movie in user.watchlist:
                in_watchlist = True
        except services.UnknownUserException:
            return redirect(url_for('authentication_bp.login'))
    add_to_watchlist = request.args.get('add_to_watchlist')
    remove_from_watchlist = request.args.get('remove_from_watchlist')
    watch_now = request.args.get('watch_now')
    if add_to_watchlist == "True" or in_watchlist or watch_now == "True":
        if 'username' in session:
            try:
                username = session['username']
                user = services.get_user(username, repo.repo_instance)
            except services.UnknownUserException:
                return redirect(url_for('authentication_bp.login'))
        else:
            return redirect((url_for('authentication_bp.login')))
        if add_to_watchlist == "True":
            user.watchlist.add_movie(target_movie)
            in_watchlist = True
        elif remove_from_watchlist == "True":
            user.watchlist.remove_movie(target_movie)
            in_watchlist = False
        if watch_now == "True":
            user.watch_movie(target_movie)
            if in_watchlist:
                user.watchlist.remove_movie(target_movie)
                in_watchlist = False
        if in_watchlist:
            list_id = 0
            for i in range(user.watchlist.size()):
                if user.watchlist.select_movie_to_watch(i) == target_movie:
                    list_id = i
                    break
            next_id = min(list_id + 1, user.watchlist.size())
            prev_id = max(list_id - 1, 0)
            next_watchlist = False
            prev_watchlist = False
            if user.watchlist.size() - (list_id + 1) >= 1:
                next_watchlist = True
            next_movie = user.watchlist.select_movie_to_watch(next_id)
            next_movie_url = None
            if next_movie is not None:
                next_movie_url = url_for('movies_bp.movie', title=next_movie.title,
                                         release_year=next_movie.release_year)
            if list_id >= 1:
                prev_watchlist = True
            prev_movie = user.watchlist.select_movie_to_watch(prev_id)
            prev_movie_url = None
            if prev_movie is not None:
                prev_movie_url = url_for('movies_bp.movie', title=prev_movie.title,
                                         release_year=prev_movie.release_year)

            target_movie = services.movie_to_dict(target_movie)
            target_movie['url'] = url_for('movies_bp.movie', title=target_title, release_year=target_year)
            target_movie['review_url'] = url_for('movies_bp.review_movie', title=target_title, release_year=target_year)
            return render_template(
                'movies/movie.html',
                movie=target_movie,
                next_watchlist=next_watchlist,
                next_movie_url=next_movie_url,
                prev_watchlist=prev_watchlist,
                prev_movie_url=prev_movie_url,
                watch_now_url=url_for('movies_bp.movie', title=target_title, release_year=target_year, watch_now=True),
                in_watchlist=True,
                add_to_watchlist_url=url_for('movies_bp.movie', title=target_title,
                                             release_year=target_year, add_to_watchlist=True),
                remove_from_watchlist_url=url_for('movies_bp.movie', title=target_title,
                                                  release_year=target_year, remove_from_watchlist=True),
                reviews_url=url_for('movies_bp.reviews', title=target_title, release_year=target_year),
                watchlist_empty=False
            )
    target_movie = services.movie_to_dict(target_movie)
    target_movie['url'] = url_for('movies_bp.movie', title=target_title, release_year=target_year)
    target_movie['review_url'] = url_for('movies_bp.review_movie', title=target_title, release_year=target_year)
    return render_template(
        'movies/movie.html',
        movie=target_movie,
        next_watchlist=False,
        next_movie_url=None,
        prev_watchlist=False,
        prev_movie_url=None,
        watch_now_url=url_for('movies_bp.movie', title=target_title, release_year=target_year, watch_now=True),
        in_watchlist=in_watchlist,
        add_to_watchlist_url=url_for('movies_bp.movie', title=target_title,
                                     release_year=target_year, add_to_watchlist=True),
        remove_from_watchlist_url=url_for('movies_bp.movie', title=target_title,
                                          release_year=target_year, remove_from_watchlist=True),
        reviews_url=url_for('movies_bp.reviews', title=target_title, release_year=target_year),
        watchlist_empty=utilities.get_watchlist_empty()
    )


@movies_blueprint.route('/reviews', methods=['GET'])
def reviews():
    target_title = request.args.get('title')
    target_year = request.args.get('release_year')
    if target_year is not None:
        target_year = int(target_year)
    target_movie = services.get_movie(target_title, target_year, repo.repo_instance)
    if target_movie is None:
        return redirect(url_for('home_bp.home'))
    review_list = services.get_reviews_for_movie(target_movie, repo.repo_instance)

    reviews_id = 0
    if request.args.get('next_id') is not None:
        reviews_id = int(request.args.get('next_id'))
    next_id = min(reviews_id + 5, len(review_list))
    prev_id = max(reviews_id - 5, 0)
    next_reviews = False
    prev_reviews = False
    if len(review_list) - (reviews_id + 1) >= 5:
        next_reviews = True
    if reviews_id >= 5:
        prev_reviews = True

    target_movie = services.movie_to_dict(target_movie)
    target_movie['url'] = url_for('movies_bp.movie', title=target_title, release_year=target_year)
    target_movie['review_url'] = url_for('movies_bp.review_movie', title=target_title, release_year=target_year)
    return render_template(
        'movies/reviews.html',
        movie=target_movie,
        reviews=review_list[reviews_id: next_id],
        prev_reviews=prev_reviews,
        prev_reviews_url=url_for('movies_bp.reviews', title=target_title, release_year=target_year, next_id=prev_id),
        next_reviews=next_reviews,
        next_reviews_url=url_for('movies_bp.reviews', title=target_title, release_year=target_year, next_id=next_id),
        watchlist_empty=utilities.get_watchlist_empty()
    )


@movies_blueprint.route('/watchlist', methods=['GET'])
@login_required
def watchlist():
    username = session['username']
    try:
        user = services.get_user(username, repo.repo_instance)

        movies_id = 0
        if request.args.get('next_id') is not None:
            movies_id = int(request.args.get('next_id'))
        next_id = min(movies_id + 6, user.watchlist.size())
        prev_id = max(movies_id - 6, 0)
        next_movies = False
        prev_movies = False
        if user.watchlist.size() - (movies_id + 1) >= 6:
            next_movies = True
        if movies_id >= 6:
            prev_movies = True

        movies = []
        for i in range(movies_id, next_id):
            movies.append(user.watchlist.select_movie_to_watch(i))
        movies = services.movies_to_dict(movies)
        for list_movie in movies:
            list_movie['url'] = url_for('movies_bp.movie', title=list_movie['title'],
                                        release_year=list_movie['release_year'])
            list_movie['review_url'] = url_for('movies_bp.review_movie', title=list_movie['title'],
                                               release_year=list_movie['release_year'])
        return render_template(
            'movies/movie_list.html',
            title="My Watchlist",
            movies=movies,
            prev_movies=prev_movies,
            prev_movies_url=url_for('movies_bp.watchlist', next_id=prev_id),
            next_movies=next_movies,
            next_movies_url=url_for('movies_bp.watchlist', next_id=next_id),
            watchlist_empty=utilities.get_watchlist_empty()
        )
    except services.UnknownUserException:
        return redirect(url_for('authentication_bp.login'))


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    rating = IntegerField('Rating', [
        DataRequired(),
        NumberRange(min=0, max=10, message='Please choose a rating from 0 to 10')])
    movie_title = HiddenField("Movie Title")
    release_year = HiddenField("Release Year")
    submit = SubmitField('Submit')
