# Import packages
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
import requests
from bs4 import BeautifulSoup
# Import application, database, and models
from app import app, db, Language, Method

# Instantiate Migrate and Manager
migrate = Migrate(app, db)
manager = Manager(app)

# Add command line arguments for database and shell with ORM context
manager.add_command('db', MigrateCommand)
def make_shell_context():
    return dict(app=app, db=db, Language=Language, Method=Method)
manager.add_command('shell', Shell(make_context=make_shell_context))

# helper methods used in the ruby method below
def get_text(html_element):
    return html_element.text

def concat_strings(element_collection):
    new_string = ""
    for text in element_collection:
        new_string += get_text(text) + "\n"
    return new_string

@manager.command
def get_ruby_methods():
    language = Language.query.filter_by(name='Ruby').first()
    if language is None:
        language = Language(name='Ruby')
        db.session.add(language)
        db.session.commit()
    URL = 'https://ruby-doc.org/core-2.6/Array.html'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    instance_methods_div = soup.find(id="public-instance-method-details")
    instance_methods = instance_methods_div.find_all('div', class_='method-detail')
    for method in instance_methods:
        method_name = method.find('a')['name']
        url = 'https://ruby-doc.org/core-2.6/Array.html#' + method_name
        method_call_seq = method.find_all('span', class_='method-callseq')
        if method_call_seq is None:
            method_call_seq = method.find('div', class_='method-heading').text
            args = method.find('div', class_='method-args')
            if args is not None:
                method_call_seq += args
            method_call_seq
        else:
            method_call_seq = concat_strings(method_call_seq)
        method_descriptions = method.find_all('p')
        method_description = concat_strings(method_descriptions)
        code_snippet = method.find('pre', class_='ruby')
        if code_snippet is None:
            code_snippet = ''
        else:
            code_snippet = code_snippet.text
        method = Method(name=method_name, docs_url=url, syntax=method_call_seq, description=method_description, snippet=code_snippet, language=language)
        db.session.add(method)
        db.session.commit()

@manager.command
def get_js_methods():
    language = Language.query.filter_by(name='JavaScript').first()
    if language is None:
        language = Language(name='JavaScript')
        db.session.add(language)
        db.session.commit()
    URL = 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    methods_div = soup.find('div', class_="quick-links")
    methods_list = methods_div.find('ol')
    method_links = methods_list.find_all('a')
    for link in method_links[6:45]:
        description = link['title']
        if "deprecated" not in description:
            name = link.find('code').text
            url = 'https://developer.mozilla.org/' + link['href']
            method_page = requests.get(url)
            method_soup = BeautifulSoup(method_page.content, 'html.parser')
            call_seq_box = method_soup.find('pre', class_='syntaxbox') #strip this?
            if call_seq_box is not None:
                call_seq = call_seq_box.text
            else:
                call_seq = method_soup.find('pre').text

            edit_box = method_soup.find('iframe')
            if edit_box is not None:
                code_page = requests.get(edit_box['src'])
                code_soup = BeautifulSoup(code_page.content, 'html.parser')

                snippet_box = code_soup.find('pre')
                if snippet_box is not None:
                    snippet = snippet_box.text
                else:
                    example_header = method_soup.find('h2', string='Examples')
                    first_example = example_header.find_next_sibling('h3')
                    snippet = first_example.find_next_sibling('pre').text
            else:
                snippet = method_soup.find('pre').text
            method = Method(name=name, docs_url=url, syntax=call_seq, description=description, snippet=snippet, language=language)
            db.session.add(method)
            db.session.commit()

if __name__ == '__main__':
    manager.run()
