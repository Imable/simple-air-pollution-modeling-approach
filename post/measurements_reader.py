import pandas
from datetime import datetime
# Hacky way to import from the `base` folder in the root of the project
import sys
sys.path.append("..")

from base.reader import Reader

class MeasurementsReader(Reader):
    def __init__(self, 
        columns,
        pm_type,
        *args, **kwargs):
        self.columns = columns
        self.pm_type = pm_type
        
        super().__init__(*args, **kwargs)

    def parse_and_clean(self, df):
        # Parse the date and time columns to the datetime format
        df['DATE'] = pandas.to_datetime(df['DATE'], errors='coerce')
    
        # Multiply PM measurements from sheet by 1000 to achieve the same unit as the model (microgram/m3)
        for column in self.columns:
            if self.pm_type in column:
                df[column] *= 1000
        
        # Only select relevant columns
        df = df[['DATE'] + self.columns]

        return df

    def fetch(self):
        return self.data