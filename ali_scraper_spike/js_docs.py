import pprint
import requests
from bs4 import BeautifulSoup
from Method import Method

URL = 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
# import code; code.interact(local=dict(globals(), **locals()))
methods_div = soup.find('div', class_="quick-links")
methods_list = methods_div.find('ol')
method_links = methods_list.find_all('a')
# need to start on method_links element 6 to start the list of methods
# 44 is probably the last method that makes sense
# there are some depricated methods in here that need to be filtered out
methods = []
for link in method_links[6:45]:
    description = link['title']
    if "deprecated" not in description:
        name = link.find('code').text
        print(name)
        url = 'https://developer.mozilla.org/' + link['href']
        method_page = requests.get(url) #have to make another request to the new site
        method_soup = BeautifulSoup(method_page.content, 'html.parser')

        call_seq_box = method_soup.find('pre', class_='syntaxbox') #strip this?
        if call_seq_box is not None:
            call_seq = call_seq_box.text
        else:
            call_seq = method_soup.find('pre').text

        edit_box = method_soup.find('iframe')
        # import code; code.interact(local=dict(globals(), **locals()))
        if edit_box is not None:
            code_page = requests.get(edit_box['src'])
            code_soup = BeautifulSoup(code_page.content, 'html.parser')

            snippet_box = code_soup.find('pre')
            if snippet_box is not None:
                snippet = snippet_box.text
            else:
                # snippet = method_soup.find('pre').text
                example_header = method_soup.find('h2', string='Examples')
                first_example = example_header.find_next_sibling('h3')
                snippet = first_example.find_next_sibling('pre').text
        else:
            # import code; code.interact(local=dict(globals(), **locals()))
            snippet = method_soup.find('pre').text

        #*************************************************************
        # previous code for examples
        # snippet - examples start under a H2 "Examples"
        # ends at an H2 called Polyfill
        # example_header = method_soup.find('h2', string='Examples')
        # example_h3s = example_header.find_next_siblings('h3')
        # snippet = ''
        # for example in example_h3s:
        #     code = example.find_next_sibling('pre').text
        #     snippet = snippet + code + '\n'
        #*************************************************************
        new_method = Method(name, url, call_seq, description, snippet)
        print(new_method.name + new_method.snippet)
        methods.append(new_method)
    methods
import code; code.interact(local=dict(globals(), **locals()))

# to iterate over siblings
    # for sibling in example_header.next_siblings:
    #     print(repr(sibling))
