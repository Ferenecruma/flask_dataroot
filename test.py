from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from sqlalchemy import inspect

from settings.constants import DB_URL
from core import db
from models.actor import Actor 
from models.movie import Movie


data_actor = {'name': 'Megan Fox', 'gender': 'female', 'date_of_birth': dt.strptime('16.05.1986', '%d.%m.%Y').date()}
data_actor_upd = {'name': 'Not Megan Fox', 'gender': 'male', 'date_of_birth': dt.strptime('16.05.2000', '%d.%m.%Y').date()}

data_movie = {'name': 'Transformers', 'genre': 'action', 'year': 2007}
data_movie_upd = {'name': 'Teenage Mutant Ninja Turtles', 'genre': 'bad movie', 'year': 2014}

app = Flask(__name__, instance_relative_config=False)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning

db.init_app(app)

with app.app_context():
    db.create_all()
    actor = Actor.create(**data_actor)
    print('created actor:', actor.__dict__, '\n')

    movie = Movie.create(**data_movie)
    print('created movie:', movie.__dict__, '\n')

    upd_actor = Actor.update(actor.id, **data_actor_upd)
    print('updated actor:', upd_actor.__dict__, '\n')

    upd_movie = Movie.update(movie.id, **data_movie_upd)
    print('updated movie:', upd_movie.__dict__, '\n')

    add_rels_actor = Actor.add_relation(actor.id, upd_movie)
    movie_2 = Movie.create(**data_movie)
    add_more_rels_actor = Actor.add_relation(actor.id, movie_2)
    print('relations list:', add_more_rels_actor.filmography, '\n')
    assert len(add_more_rels_actor.filmography) == 2

    clear_rels_actor = Actor.clear_relations(actor.id)
    print('all relations cleared:', clear_rels_actor.filmography, '\n')
    assert clear_rels_actor.filmography == []

    del_actor = Actor.delete(actor.id)
    assert del_actor == 1

    db.drop_all()