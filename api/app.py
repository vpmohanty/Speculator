# TODO: Add private API with Redis Cache and PostgreSQL (or any SQL DB with SQLAlchemy)
from api import api, cache, db
from flask import abort, Flask
from flask_restful import Resource
from os import getenv
from api.resources.market_json import MarketJsonItem, MarketList
from api.resources.trend import Predict

def setup_app():
    db_uri = getenv('SQLALCHEMY_DATABASE_URI') # format: postgresql://user:pw@host:port/db
    if not db_uri:
        abort(401)

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        api.init_app(app)

    return app

def setup_db(application, sqlalchemy_bind, mem_cache=None):
    with application.app_context():
        if mem_cache is not None:
            mem_cache.init_app(app)
        sqlalchemy_bind.init_app(app)
        sqlalchemy_bind.create_all()

if __name__=='__main__':
    app = setup_app()

    from api.models import * # Load all DB models
    setup_db(app, db, mem_cache=cache)

    app.run(debug=True)
