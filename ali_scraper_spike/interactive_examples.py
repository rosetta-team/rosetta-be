import requests
from bs4 import BeautifulSoup
from Method import Method

URL = 'https://interactive-examples.mdn.mozilla.net/pages/js/array-from.html'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
snippet = soup.find('pre').text

import code; code.interact(local=dict(globals(), **locals()))
