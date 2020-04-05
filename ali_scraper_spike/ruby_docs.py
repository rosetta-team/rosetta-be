import pprint
import requests
from bs4 import BeautifulSoup
from Method import Method

URL = 'https://ruby-doc.org/core-2.6/Array.html'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
# here are all of our methods
# methods = soup.find_all('div', class_='method-detail')

# a better way to get all methods is to use
# id=public-instance-method-details
instance_methods_div = soup.find(id="public-instance-method-details")
instance_methods = instance_methods_div.find_all('div', class_='method-detail')
# this would be for one method
map = soup.find(id="map-method")
# first_method = methods[0]
# not every method has a class "method-name"
# first_method_name = first_method.find('span', class_="method-name").text
# first_method_alt_name = first_method.find('a')['name']

# helper methods used below
def get_text(html_element):
    return html_element.text

def make_description(description_text):
    description = ""
    for text in description_text:
        description += get_text(text) + "\n"
    return description

# to loop over all the methods and start doing something w/ them...

# method_names = []
methods = []
for method in instance_methods:
    method_name = method.find('a')['name']
    method_call_seq = method.find_all('span', class_='method-callseq')
    if method_call_seq is None:
        method_call_seq = method.find('div', class_='method-heading').text
        args = method.find('div', class_='method-args')
        if args is not None:
            method_call_seq += args
            # still missing 'append(*args)'
        method_call_seq
    else:
        # method_call_seq = method_call_seq.text
        method_call_seq = make_description(method_call_seq)

    method_descriptions = method.find_all('p')
    method_description = make_description(method_descriptions)
    code_snippet = method.find('pre', class_='ruby')
    if code_snippet is None:
        code_snippet = ''
    else:
        code_snippet = code_snippet.text
#     # method_name = method.find('span', class_="method-callseq").text
#     # if None in method_name:
#         # method_name = method.find('span', class_="method-name").text
    methods.append(Method(method_name, method_call_seq, method_description, code_snippet))
    # method_names.append(method_name)

# description_text = instance_methods[0].find_all('p')
import code; code.interact(local=dict(globals(), **locals()))

for i, val in enumerate(methods):
    print(val.call_seq)

for i, val in enumerate(methods):
    print(val.description)

for i, val in enumerate(methods):
    print(val.name)

for i, val in enumerate(methods):
    print(val.snippet)
