import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask

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

    @app.route('/')
    def root():
        return 'Welcome to the Rosetta backend server!'

    return app

# Instantiate Flask app and SQLAlchemy ORM
app = create_app()
db = SQLAlchemy(app)

# Define models in relation to instantiated ORM
class Language(db.Model):
    __tablename__ = 'languages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    methods = db.relationship('Method', backref='language')

    def __repr__(self):
        return '<Language %r>' % self.name

class Method(db.Model):
    __tablename__ = 'methods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    snippet = db.Column(db.Text)
    syntax = db.Column(db.Text)
    description = db.Column(db.Text)
    docs_url = db.Column(db.String)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'))

    def __repr__(self):
        return '<Method %r>' % self.name