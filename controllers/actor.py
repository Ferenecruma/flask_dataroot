from flask import jsonify, make_response

from datetime import datetime as dt
from ast import literal_eval

from models.actor import Actor
from models.movie import Movie
from settings.constants import ACTOR_FIELDS     # to make response pretty
from .parse_request import get_request_data


def get_all_actors():
    """
    Get list of all records
    """  
    all_actors = Actor.query.all()
    actors = []
    for actor in all_actors:
        act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        actors.append(act)
    return make_response(jsonify(actors), 200) 

  
def get_actor_by_id():
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

        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400) 

        return make_response(jsonify(actor), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400) 


def add_actor():
    """
    Add new actor
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if all(key in data.keys() for key in ACTOR_FIELDS[1:]):
        try:
            data['date_of_birth'] = dt.strptime(data['date_of_birth'], '%d.%m.%Y').date()
        except ValueError:
            err = 'Not a valid date'
            return make_response(jsonify(error=err), 400)
        new_record = Actor.create(**data)
    else:
        err = 'Not valid record to add'
        return make_response(jsonify(error=err), 400) 

    # use this for 200 response code
    new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
    return make_response(jsonify(new_actor), 200)
    ### END CODE HERE ###


def update_actor():
    """
    Update actor record by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if all(key in ACTOR_FIELDS for key in data.keys()) and 'id' in data.keys():
        try:
            if 'date_of_birth' in data:
                data['date_of_birth'] = dt.strptime(data['date_of_birth'], '%d.%m.%Y').date()
            row_id = int(data['id'])
            del data['id']
            upd_record = Actor.update(row_id, **data)
        except ValueError:
            err = 'Not a valid data'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'Not valid record to add'
        return make_response(jsonify(error=err), 400) 
    # use this for 200 response code
    upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}
    return make_response(jsonify(upd_actor), 200)
    ### END CODE HERE ###

def delete_actor():
    """
    Delete actor by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' in data:
        try:
            row_id = int(data['id'])
        except ValueError:
            err = 'Not a valid request'
            return make_response(jsonify(error=err), 400)
        res = Actor.delete(row_id)
    else:
        err = 'Not a valid request'
        return make_response(jsonify(error=err), 400)
    # use this for 200 response code
    msg = 'Record successfully deleted'
    return make_response(jsonify(message=msg), 200)
    ### END CODE HERE ###


def actor_add_relation():
    """
    Add a movie to actor's filmography
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
        rel = Movie.query.filter_by(id=rel_row_id).first()
        if rel:
            actor = Actor.add_relation(row_id, rel)  # add relation here
        else:
            msg = "Relation doesn't exist"
            make_response(jsonify(error=msg), 400)
    else:
        msg = "Not a valid request"
        return make_response(jsonify(error=msg), 400)
    # use this for 200 response code
    
    rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
    rel_actor['filmography'] = str(actor.filmography)
    return make_response(jsonify(rel_actor), 200)
    ### END CODE HERE ###


def actor_clear_relations():
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
        actor = Actor.clear_relations(row_id)  # clear relations here
        if not actor:
            err = "Actor doesn't exist"
            return make_response(jsonify(error=err), 400)
    else:
        msg = "Not a valid request"
        return make_response(jsonify(error=msg), 400)

    # use this for 200 response code    
    rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
    rel_actor['filmography'] = str(actor.filmography)
    return make_response(jsonify(rel_actor), 200)
    ### END CODE HERE ###
