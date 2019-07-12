"""A HTML parser using BeautifulSoup4, Pandas and requests.

Scraps and parses a html file to extract an user-defined element type,
and parses this. For tables, it converts the html table to a pandas DataFrame.

Based on https://srome.github.io/Parsing-HTML-Tables-in-Python-with-BeautifulSoup-and-pandas/
"""

import requests
import pandas as pd
import bs4 as bs

class HTMLParser:

    def __init__(self, url):
        """
        :Input:
         :url: ``String`` of a url to be parsed
        """
        self.url = url

    def scrap_url(self):
        """Scraps and returns the URL set during the initialisation
        """
        response = requests.get(self.url)
        page = bs.BeautifulSoup(response.text, 'lxml')
        return page

    def get_page_elements(self, page, element='table', params = {}):
        """Extracts all elements of type <element> from the given page
        :Input:
         :page: ``bs4.BeautifulSoup`` of scrapped webpage
         :element: ``String`` (default: ``"table"``) of webpage element to search for
         :params: ``Dictionary`` (default: ``{}``) to narrow down the search of elements, e.g. ``params={"class": "mytable", "id": "stockprices"}
        :Output:
         :page_elements: ``List`` of elements found in ``page``
        """
        page_elements = page.find_all(element, params)
        return page_elements

    def parse_html_table(self, table):
        """Parses a ``bs4.BeautifulSoup`` object (expected to be a table only!)
        and converts it into a pandas.DataFrame.
        :Input:
         :table: ``bs4.BeautifulSoup``, must only contain a table in html syntax
        :Output:
         :df: ``pandas.DataFrame`` which holds the content of the given html table
        """
        n_columns = 0
        n_rows=0
        column_names = []

        # Find number of rows and columns
        # we also find the column titles if we can
        for row in table.find_all('tr'):

            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows = n_rows + 1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)

            # Handle column names if we find them
            th_tags = row.find_all('th') 
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text().strip())

        # Safeguard on Column Titles
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")

        # Assembling DataFrame
        columns = column_names if len(column_names) > 0 else range(0,n_columns)
        df = pd.DataFrame(columns = columns,
                          index= range(0,n_rows))
        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[row_marker,column_marker] = column.get_text().strip()
                column_marker = column_marker + 1
            if len(columns) > 0:
                row_marker = row_marker + 1

        # Convert to float if possible
        for col in df:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                pass

        return df
