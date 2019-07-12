<p align="left">
  <a href="https://www.python.org/download/releases/3.0/">
    <img src="https://img.shields.io/badge/python-3+-brightgreen.svg?style=popout" alt='python'>
  </a>
  <a href="https://github.com/fmilthaler/HTMLParser/blob/master/LICENSE.txt">
    <img src="https://img.shields.io/github/license/fmilthaler/HTMLParser.svg?style=popout" alt="license">
  </a>
</p>

# HTMLParser
*HTMLParser* is a class for scrapping and parsing a webpage. Especially useful for converting a table in HTML syntax to a `pandas.DataFrame`.

## Example
Here we scrap a page from Wikipedia, parse it for tables, and convert the first table found into a `pandas.DataFrame`.

```
from htmlparser.htmlparser import HTMLParser
import pandas

# Here we scrap a page from Wikipedia, parse it for tables, and convert the first table found into a `pandas.DataFrame`.
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
hp = HTMLParser(url)
# scrapping the webpage
page = hp.scrap_url()
# extracting only tables from the webpage
element = 'table'
params = {'class': 'wikitable sortable'}
elements = hp.get_page_elements(page, element=element, params=params)
# get a pandas.DataFrame from the (first) html table
df = hp.parse_html_table(elements[0])
print(df.columns.values)
```

This results in the following output (column headers):

```
['Symbol' 'Security' 'SEC filings' 'GICS Sector' 'GICS Sub Industry'
 'Headquarters Location' 'Date first added' 'CIK' 'Founded']
```

