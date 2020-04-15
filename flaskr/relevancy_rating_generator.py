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
            description_comparer = DescriptionComparer()
            method_result = MethodResult(method_id=method.id, search_result_id=result.id)
            
            # method.name
            # result.method.name
            method_1_info = {'description':method.description, 'name':method.name}
            method_2_info = {'description':result.method.description, 'name':result.method.name}
            description_rating = description_comparer.compare(method_1_info['description'], method_2_info['description'])
            name_rating = description_comparer.compare(method_1_info['name'], method_2_info['name'])
            
            method_result.relevance_rating_desciption = description_rating
            method_result.relevance_rating_title = name_rating
            method_result.weighted_relevancy_rating = calc_weighted_relevancy_rating(description_rating, name_rating)
            if method_result.weighted_relevancy_rating > .06:  
                db.session.add(method_result)
                db.session.commit()

def generate_relevancy_ratings():
    method_results = MethodResult.query.all()
    description_comparer = DescriptionComparer()
    for result in method_results:
        method_1_info = {'description':result.method.description, 'name':result.method.name}
        method_2_info = {'description':result.search_result.method.description, 'name':result.search_result.method.name}

        description_rating = description_comparer.compare(method_1_info['description'], method_2_info['description'])
        name_rating = description_comparer.compare(method_1_info['name'], method_2_info['name'])
        result.relevance_rating_desciption = description_rating
        result.relevance_rating_title = name_rating
        result.weighted_relevancy_rating = calc_weighted_relevancy_rating(description_rating, name_rating)
        db.session.commit()

def calc_weighted_relevancy_rating(description, name):
    if name >= 0.7:
        return ((name * 8) + (description * 2)) / 10
    else:
        return ((name * 2) + (description * 8)) / 10 

def remove_non_relevant_rows():
    # # MethodResult.delete(MethodResult).where(MethodResult.c.relevance_rating_title <= .3.exucute()
    # print("hi")
    # method_results = MethodResult.query.all()
    # # d = MethodResult.query.filter_by(relevance_rating_title <= .3)
    breakpoint()



# generate_search_results()
generate_method_results()
# generate_relevancy_ratings()
# remove_non_relevant_rows() 
