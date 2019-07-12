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
