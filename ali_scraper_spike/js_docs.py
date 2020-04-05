import pprint
import requests
from bs4 import BeautifulSoup
from Method import Method

URL = 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
import code; code.interact(local=dict(globals(), **locals()))
methods_div = soup.find('div', class_="quick-links")
methods_list = methods_div.find('ol')
method_links = methods_list.find_all('a')
# need to start on method_links element 6 to start the list of methods
# 44 is probably the last method that makes sense
# there are some depricated methods in here that need to be filtered out
methods = []
for link in method_links[6:45]:
    description = link['title']
    name = link.find('code').text
    call_seq = '' #this is in a different part of the page
    snippet = '' #most methods would inolve actually going to another page to get a snippet
    # the snippets are then held in a github repo
    if "deprecated" not in description:
        # print(link.find('code').text)
        # print(link['title'])
        methods.append(Method(name, call_seq, description, snippet))
    methods
