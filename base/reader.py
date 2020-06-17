import pandas
from datetime import datetime

BASE_PATH = './input'

class Reader:
    def __init__(self, fname, 
            start_ts, end_ts, step,
            header_rows):

        self.start_ts = start_ts
        self.end_ts   = end_ts
        self.step     = step

        self.data = pandas.read_excel(self.__get_path(fname), header=header_rows)
        self.data = self.parse_and_clean(self.data)
        # Remove the rows that precede the timeframe
        mask      = (self.data['DATE'] >= start_ts) & (self.data['DATE'] <= end_ts)
        self.data = self.data.loc[mask]
    
    def __get_path(self, fname):
        return f'{ BASE_PATH }/{ fname }'
     
    def get_row_at(self, position):
        return self.data.iloc[[position]]