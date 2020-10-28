from flask import jsonify, make_response

from ast import literal_eval

from models.actor import Actor 
from models.movie import Movie
from settings.constants import MOVIE_FIELDS
from .parse_request import get_request_data


def get_all_movies():
    """
    Get list of all records
    """
    all_movies = Movie.query.all()
    movies = []
    for movie in all_movies:
        act = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(act)
    return make_response(jsonify(movies), 200) 

def get_movie_by_id():
    """
    Get record by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400) 

        obj = Movie.query.filter_by(id=row_id).first()
        try:
            movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400) 

        return make_response(jsonify(movie), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

def add_movie():
    """
    Add new movie
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if all(key in data.keys() for key in MOVIE_FIELDS[1:]):
        try:
            data['year'] = int(data['year'])
        except ValueError:
            err = 'Not a valid year'
            return make_response(jsonify(error=err), 400)
        new_record = Movie.create(**data)
    else:
        err = 'Not valid record to add'
        return make_response(jsonify(error=err), 400) 

    # use this for 200 response code
    new_movie = {k: v for k, v in new_record.__dict__.items() if k in MOVIE_FIELDS}
    return make_response(jsonify(new_movie), 200)
    ### END CODE HERE ###

def update_movie():
    """
    Update movie record by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if all(key in ACTOR_FIELDS for key in data.keys()) and 'id' in data.keys():
        try:
            if 'year' in data:
                data['year'] = int(data['year'])
            row_id = int(data['id'])
            del data['id']
            upd_record = Movie.update(row_id, **data)
        except ValueError:
            err = 'Not a valid data'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'Not valid record to add'
        return make_response(jsonify(error=err), 400) 
    # use this for 200 response code
    upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in MOVIE_FIELDS}
    return make_response(jsonify(upd_actor), 200)
    ### END CODE HERE ###

def delete_movie():
    """
    Delete movie by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' in data:
        try:
            row_id = int(data['id'])
        except ValueError:
            err = 'Not a valid request'
            return make_response(jsonify(error=err), 400)
        res = Movie.delete(row_id)
    else:
        err = 'Not a valid request'
        return make_response(jsonify(error=err), 400)
    # use this for 200 response code
    msg = 'Record successfully deleted'
    return make_response(jsonify(message=msg), 200)
    ### END CODE HERE ###

def movie_add_relation():
    """
    Add actor to movie's cast
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if ['id', 'ralation_id'] in data:
        try:
            row_id = int(data['id'])
            rel_row_id = int(data['relation_id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400) 
        rel = Actor.query.filter_by(id=rel_row_id).first()
        if rel:
            movie = Movie.add_relation(row_id, rel)  # add relation here
        else:
            msg = "Relation doesn't exist"
            make_response(jsonify(error=msg), 400)
    else:
        msg = "Not a valid request"
        return make_response(jsonify(error=msg), 400)
    # use this for 200 response code
    
    rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
    rel_movie['cast'] = str(movie.filmography)
    return make_response(jsonify(rel_movie), 200)

def movie_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' in data:
        try:
            row_id = int(data['id'])
        except ValueError:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        movie = Movie.clear_relations(row_id)  # clear relations here
        if not actor:
            err = "Movie doesn't exist"
            return make_response(jsonify(error=err), 400)
    else:
        msg = "Not a valid request"
        return make_response(jsonify(error=msg), 400)

    # use this for 200 response code    
    rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
    rel_movie['cast'] = str(movie.filmography)
    return make_response(jsonify(rel_movie), 200)