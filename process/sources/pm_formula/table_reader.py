import pandas

import sys
sys.path.append("....")

from base.reader import BASE_PATH
FNAME = 'ship_specific_data.xlsx'

class TableReader:

    def __init__(self):
        self.data = pandas.read_excel(self.__get_path())

    def __get_path(self):
        return f'{ BASE_PATH }/{ FNAME }'
         
    def fetch_row(self, ship_name):
        return self.data.loc[self.data['NAME'] == 'Hurtigruten'].squeeze()

table_reader = TableReader()
