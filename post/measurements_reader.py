import pandas
from datetime import datetime
# Hacky way to import from the `base` folder in the root of the project
import sys
sys.path.append("..")

from base.reader import Reader

class MeasurementsReader(Reader):
    def __init__(self, 
        columns,
        *args, **kwargs):
        self.columns = columns
        
        super().__init__(*args, **kwargs)

    def parse_and_clean(self, df):
        # Parse the date and time columns to the datetime format
        df['DATE'] = pandas.to_datetime(df['DATE'], errors='coerce')
    
        # Drop the rows that do not have a valid date or time
        # for column in self.columns:
        #     df = df.dropna(subset=df[column])

        # Only select relevant columns
        df = df[['DATE'] + self.columns]

        return df

    def fetch(self):
        return self.data