import pandas
from datetime import datetime
# Hacky way to import from the `base` folder in the root of the project
import sys
sys.path.append("..")

from base.reader import Reader

class MeasurementsReader(Reader):
    def __init__(self, 
        pm_type, station,
        *args, **kwargs):
        self.columns = [f'{s}_{pm_type}' for s in station]
        
        super().__init__(*args, **kwargs)

    def parse_and_clean(self, df):
        '''
        Convert used times and dates to their respective formats and remove the rows that do not comply with specific types and formats.
        '''

        # Parse the date and time columns to the datetime format
        df['DATE'] = pandas.to_datetime(df['DATE'], errors='coerce')
    
        # Drop the rows that do not have a valid date or time
        df = df.dropna(subset=['DATE'])

        # Only select relevant columns
        df = df[['DATE'] + self.columns]

        return df