import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
from flask_graphql import GraphQLView

from .models import db_session
from .schema import schema, Language

# App factory method to create instance of Flask app
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config = True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/rosetta_dev",
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )



    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #####
    # this might be define a route?
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True # for having the GraphiQL interface
        )
    )
    @app.route('/')
    def root():
        return 'Welcome to the Rosetta backend server!'

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app

# Instantiate Flask app and SQLAlchemy ORM
app = create_app()
db = SQLAlchemy(app)
