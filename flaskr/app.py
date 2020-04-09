import os
import graphene
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView

load_dotenv()
# App factory method to create instance of Flask app
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config = True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL"),
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

class SearchResult(db.Model):
    __tablename__ = 'search_results'

    id = db.Column(db.Integer, primary_key=True)
    method_id = db.Column(db.Integer, db.ForeignKey('methods.id'))
    target_language_id = db.Column(db.Integer, db.ForeignKey('languages.id'))
    source_language_id = db.Column(db.Integer, db.ForeignKey('languages.id'))

    def __repr__(self):
        return '<SearchResult %r' % self.id

class MethodResult(db.Model):
    __tablename__ = 'method_results'

    id = db.Column(db.Integer, primary_key=True)
    method_id = db.Column(db.Integer, db.ForeignKey('methods.id'))
    search_result_id = db.Column(db.Integer, db.ForeignKey('search_results.id'))
    relevance_rating = db.Column(db.Float)

    method = db.relationship('Method', backref='method_results')
    search_result = db.relationship('SearchResult', backref='method_results')

    def __repr__(self):
        return '<MethodResult %r' % self.id

# schema objects
class MethodObject(SQLAlchemyObjectType):
    class Meta:
        model = Method
        interfaces = (graphene.relay.Node, )

class LanguageObject(SQLAlchemyObjectType):
    class Meta:
        model = Language
        interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_methods = SQLAlchemyConnectionField(MethodObject)
    all_languages = SQLAlchemyConnectionField(LanguageObject)

schema = graphene.Schema(query=Query)

# additional routes, needs to come after schema is defined
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)
