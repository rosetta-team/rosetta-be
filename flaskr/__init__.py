import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from model import db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config = True)
    db.init_app(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
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
    def route():
        return 'Welcome to the Rosetta backend server!'

    return app
