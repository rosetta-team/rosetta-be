from app import app, db, Language, Method, SearchResult, MethodResult
from lib.description_comparer import DescriptionComparer
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

def generate_search_results():
    js_methods = Method.query.filter_by(language_id=2)
    ruby_methods = Method.query.filter_by(language_id=1)

    for method in js_methods:
        search_result = SearchResult(target_language_id=1, source_language_id=2, method_id=method.id)
        db.session.add(search_result)
        db.session.commit()

    for method in ruby_methods:
        search_result = SearchResult(target_language_id=2, source_language_id=1, method_id=method.id)
        db.session.add(search_result)
        db.session.commit()

def generate_method_results():
    search_results = SearchResult.query.all()
    js_methods = Method.query.filter_by(language_id=2)
    ruby_methods = Method.query.filter_by(language_id=1)

    for result in search_results:
        methods = Method.query.filter_by(language_id=result.target_language_id)
        for method in methods:
            method_result = MethodResult(method_id=method.id, search_result_id=result.id)
            db.session.add(method_result)
            db.session.commit()

def generate_relevancy_ratings():
    method_results = MethodResult.query.all()
    description_comparer = DescriptionComparer()
    for result in method_results:
        description_1 = result.method.description
        description_2 = result.search_result.method.description

        rating = description_comparer.compare(description_1, description_2)
        result.relevance_rating = rating
        db.session.commit()


generate_search_results()
generate_method_results()
generate_relevancy_ratings()
