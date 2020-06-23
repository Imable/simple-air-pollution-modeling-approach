import pandas

class TableReader:

    def __init__(self):
        file_path = f'./input/ship_specific_data.xlsx'
        self.data = pandas.read_excel(file_path)
         
    def fetch_row(self, ship_name):
        return self.data.loc[self.data['NAME'] == 'Hurtigruten'].squeeze()

table_reader = TableReader()
