import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask

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

    @app.route('/')
    def root():
        return 'Welcome to the Rosetta backend server!'

    return app


app = create_app()
db = SQLAlchemy(app)
from model import Language
# migrate = Migrate(app, db)
