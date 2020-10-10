from flask import Blueprint, url_for, request, render_template
from werkzeug.utils import redirect

from flix.adapters import repository as repo
import flix.search.services as services
from flix.utilities import utilities

search_blueprint = Blueprint('search_bp', __name__)


@search_blueprint.route('/search_for_director', methods=['GET', 'POST'])
def search_for_director():
    target_director = None
    search_form = utilities.SearchForm()
    search_form.search_term.label = "Search for Director"
    if search_form.validate_on_submit():
        target_director = search_form.search_term.data
        return redirect(url_for('search_bp.search_for_director', director=target_director))

    if request.method == 'GET':
        target_director = request.args.get('director')

    directors = []
    title = ""
    if target_director is not None and len(target_director.strip()) > 0:
        directors = services.get_directors_by_name(target_director, repo.repo_instance)
        for director in directors:
            director['movies_url'] = url_for('movies_bp.movies_by_director', director=director['name'])
        title += 'Search Results For: "' + target_director + '"'

    items_id = 0
    if request.args.get('next_id') is not None:
        items_id = int(request.args.get('next_id'))
    next_id = min(items_id + 8, len(directors))
    prev_id = max(items_id - 8, 0)
    next_items = False
    prev_items = False
    if len(directors) - (items_id + 1) >= 8:
        next_items = True
    if items_id >= 8:
        prev_items = True

    return render_template(
        'search/search.html',
        search_form=search_form,
        handler_url=url_for('search_bp.search_for_director', director=target_director),
        title=title,
        search_list=directors[items_id: next_id],
        prev_items=prev_items,
        prev_items_url=url_for('search_bp.search_for_director', director=target_director, next_id=prev_id),
        next_items=next_items,
        next_items_url=url_for('search_bp.search_for_director', director=target_director, next_id=next_id),
        watchlist_empty=utilities.get_watchlist_empty()
    )


@search_blueprint.route('/search_for_actor', methods=['GET', 'POST'])
def search_for_actor():
    target_actor = None
    search_form = utilities.SearchForm()
    search_form.search_term.label = "Search for Actor"
    if search_form.validate_on_submit():
        target_actor = search_form.search_term.data
        return redirect(url_for('search_bp.search_for_actor', actor=target_actor))

    if request.method == 'GET':
        target_actor = request.args.get('actor')

    actors = []
    title = ""
    if target_actor is not None and len(target_actor.strip()) > 0:
        colleagues = request.args.get('colleagues')
        if colleagues == "True":
            actors = services.get_colleagues(target_actor, repo.repo_instance)
            title = "Colleagues For:"
        else:
            actors = services.get_actors_by_name(target_actor, repo.repo_instance)
        for actor in actors:
            actor['movies_url'] = url_for('movies_bp.movies_by_actor', actor=actor['name'])
            actor['colleagues_url'] = url_for('search_bp.search_for_actor', actor=actor['name'], colleagues=True)
        title += 'Search Results For: "' + target_actor + '"'

    items_id = 0
    if request.args.get('next_id') is not None:
        items_id = int(request.args.get('next_id'))
    next_id = min(items_id + 6, len(actors))
    prev_id = max(items_id - 6, 0)
    next_items = False
    prev_items = False
    if len(actors) - (items_id + 1) >= 6:
        next_items = True
    if items_id >= 6:
        prev_items = True

    return render_template(
        'search/search.html',
        search_form=search_form,
        handler_url=url_for('search_bp.search_for_actor', actor=target_actor),
        title=title,
        search_list=actors[items_id: next_id],
        prev_items=prev_items,
        prev_items_url=url_for('search_bp.search_for_actor', actor=target_actor, next_id=prev_id),
        next_items=next_items,
        next_items_url=url_for('search_bp.search_for_actor', actor=target_actor, next_id=next_id),
        watchlist_empty=utilities.get_watchlist_empty()
    )


@search_blueprint.route('/search_for_genre', methods=['GET', 'POST'])
def search_by_genre():
    genres = services.get_genres(repo.repo_instance)
    for genre in genres:
        genre['movies_url'] = url_for('movies_bp.movies_by_genre', genre=genre['name'])

    title = "Search by Genre:"
    items_id = 0
    if request.args.get('next_id') is not None:
        items_id = int(request.args.get('next_id'))
    next_id = min(items_id + 8, len(genres))
    prev_id = max(items_id - 8, 0)
    next_items = False
    prev_items = False
    if len(genres) - (items_id + 1) >= 8:
        next_items = True
    if items_id >= 8:
        prev_items = True

    return render_template(
        'search/search.html',
        title=title,
        search_list=genres[items_id: next_id],
        prev_items=prev_items,
        prev_items_url=url_for('search_bp.search_by_genre', next_id=prev_id),
        next_items=next_items,
        next_items_url=url_for('search_bp.search_by_genre', next_id=next_id),
        watchlist_empty=utilities.get_watchlist_empty()
    )
