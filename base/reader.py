import pandas
from datetime import datetime

BASE_PATH = './input'

class Reader:
    def __init__(self, fname, 
            start_ts, end_ts, step,
            mask=True,
            header_rows=0,
            sheet=0):

        self.start_ts = start_ts
        self.end_ts   = end_ts
        self.step     = step

        self.data = pandas.read_excel(self.__get_path(fname), header=header_rows, sheet_name=sheet)

        self.data = self.parse_and_clean(self.data)

        if mask:
            # Remove the rows that precede the timeframe
            self.data = self.data.loc[start_ts:end_ts]

        self.max_row = len(self.data.index)
        

    def __get_path(self, fname):
        return f'{ BASE_PATH }/{ fname }'
     
    def row_is_not_last_row(self, position):
        '''
        Check if we already reached the end of the file
        '''
        return position < len(self.data.index) - 1

    def get_row_at(self, position):
        return self.data.iloc[[position]]