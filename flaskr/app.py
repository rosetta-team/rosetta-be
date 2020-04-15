import os
import graphene
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView
from flask_cors import CORS
from sqlalchemy import desc

load_dotenv()
# App factory method to create instance of Flask app
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config = True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL"),
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def root():
        return 'Welcome to the Rosetta backend server!'

    return app

# Instantiate Flask app and SQLAlchemy ORM and CORS
app = create_app()
db = SQLAlchemy(app)
cors = CORS(app, origins=['https://rosetta-fe.herokuapp.com','http://localhost:3000'])

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

    method = db.relationship('Method', backref='search_results')

    def __repr__(self):
        return '<SearchResult %r' % self.id

class MethodResult(db.Model):
    __tablename__ = 'method_results'

    id = db.Column(db.Integer, primary_key=True)
    method_id = db.Column(db.Integer, db.ForeignKey('methods.id'))
    search_result_id = db.Column(db.Integer, db.ForeignKey('search_results.id'))
    relevance_rating_description = db.Column(db.Float)
    relevance_rating_title = db.Column(db.Float)
    weighted_relevancy_rating = db.Column(db.Float)
    user_score = db.Column(db.Float)

    method = db.relationship('Method', backref='method_results')
    search_result = db.relationship('SearchResult', backref='method_results')

    def __repr__(self):
        return '<MethodResult %r' % self.id

    def calc_weighted_relevancy_rating(self):
        if self.relevance_rating_title >= 0.7:
            return ((self.relevance_rating_title * 8) + (self.relevance_rating_description * 2)) / 10
        else:
            return self.relevance_rating_description

class UserVote(db.Model):
    __tablename__ = 'user_votes'

    id = db.Column(db.Integer, primary_key=True)
    method_result_id = db.Column(db.Integer, db.ForeignKey('method_results.id'))
    type = db.Column(db.String)

    method_result = db.relationship('MethodResult', backref='user_votes')

# schema objects
class MethodObject(SQLAlchemyObjectType):
    class Meta:
        model = Method
        interfaces = (graphene.relay.Node, )

    id = graphene.NonNull(graphene.ID)

class LanguageObject(SQLAlchemyObjectType):
    class Meta:
        model = Language
        interfaces = (graphene.relay.Node, )

    methods = graphene.List(MethodObject)
    id = graphene.NonNull(graphene.ID)

class SearchResultObject(SQLAlchemyObjectType):
    class Meta:
        model = SearchResult
        interfaces = (graphene.relay.Node, )

class MethodResultObject(SQLAlchemyObjectType):
    class Meta:
        model = MethodResult
        interfaces = (graphene.relay.Node, )

class UserVoteObject(SQLAlchemyObjectType):
    class Meta:
        model = UserVote
        interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_methods = SQLAlchemyConnectionField(MethodObject)
    all_languages = graphene.Field(lambda: graphene.List(LanguageObject))
    translations = graphene.Field(lambda: graphene.List(MethodResultObject),
                                  method_id=graphene.Int(required=True),
                                  target_language_id=graphene.Int(required=True))

    def resolve_all_languages(parent, info):
        return Language.query.all();

    def resolve_translations(parent, info, method_id, target_language_id):
        return MethodResult.query.join(Method, MethodResult.method_id == Method.id).\
            join(SearchResult, MethodResult.search_result_id == SearchResult.id).\
            filter_by(target_language_id = target_language_id, method_id = method_id).\
            order_by(desc(MethodResult.weighted_relevancy_rating)).\
            limit(5).all()


class CreateVote(graphene.Mutation):
    class Arguments:
        method_result_id = graphene.NonNull(graphene.ID)
        type = graphene.String(required=True)

    vote = graphene.Field(lambda: UserVoteObject)
    def mutate(self, info, method_result_id, type):
        method_result = MethodResult.query.find(id=method_result_id)
        vote = UserVote(method_result_id=method_result.id, type=type)
        db.session.add(vote)
        db.session.commit()
        self.update_relevancy(method_result)

    def update_relevancy(self, method_result):
        score_percentage = ((len(method_result.user_votes.filter_by(type='up'))) / len(method_result.user_votes))
        new_weighted_relevancy_rating = (score_percentage * 0.5) + (method_result.calc_weighted_relevancy_rating() * 0.5)
        method_result.weighted_relevancy_rating = new_weighted_relevancy_rating
        db.session.commit()

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
