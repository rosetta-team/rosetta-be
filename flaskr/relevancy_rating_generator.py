from app import app, db, Language, Method, SearchResult, MethodResult
from lib.description_comparer import DescriptionComparer
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

def search_result_generator():
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
    fake_array = []

    for result in search_results:
        methods = Method.query.filter_by(language_id=result.target_language_id)
        for method in methods:
            method_result = MethodResult(method_id=method.id, search_result_id=result.id)
            fake_array.append(method_result)
            db.session.add(method_result)
            db.session.commit()
