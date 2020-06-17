import pandas
from datetime import datetime
# Hacky way to import from the `base` folder in the root of the project
import sys
sys.path.append("..")

from base.reader import Reader

class MeasurementsReader(Reader):

    def parse_and_clean(self, df):
        '''
        Convert used times and dates to their respective formats and remove the rows that do not comply with specific types and formats.
        '''

        # Parse the date and time columns to the datetime format
        df['DATE'] = pandas.to_datetime(df['DATE'], errors='coerce')
    
        # Drop the rows that do not have a valid date or time
        df = df.dropna(subset=['DATE'])

        return df
        
        # total_rows = len(df.index)

        # # Parse the date and time columns to the datetime format
        # df['DATE'] = pandas.to_datetime(df['DATE'], errors='coerce')
        # df['ETA']  = pandas.to_datetime(df['ETA'], format='%H:%M', errors='coerce')
        # df['ETD']  = pandas.to_datetime(df['ETD'], format='%H:%M', errors='coerce')
    
        # # Drop the rows that do not have a valid date or time
        # df = df.dropna(subset=['DATE'])
        # df = df.dropna(subset=['ETA'])
        # df = df.dropna(subset=['ETD'])

        # # Add the date to times in order to cope with a timestep bigger than 1 day
        # df['ETA'] = df.apply(lambda r : datetime.combine(r['DATE'], r['ETA'].time()), 1)
        # df['ETD'] = df.apply(lambda r : datetime.combine(r['DATE'], r['ETD'].time()), 1)

        # # Guarantee sorting on date column
        # df = df.sort_values(by=['DATE'])
        
        # # Count omitted rows
        # new_total_rows = len(df.index)
        # omitted_rows = new_total_rows - total_rows
        # print(f'Omitted { -omitted_rows } rows due to unparsable dates and times. (= {round(omitted_rows / total_rows * 100, 2)}%)')
        # print('____________________________________')
        # print('')

        # return df