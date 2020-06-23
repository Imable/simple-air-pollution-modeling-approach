import pandas
from datetime import datetime, timedelta
# Hacky way to import from the `base` folder in the root of the project
import sys
sys.path.append("....")

from base.reader import Reader
from ..source.ship.ship import Ship

MANOUVERING_TIME = timedelta(minutes=30)

class SourceReader(Reader):

    def __init__(self, *args, **kwargs):
        self.pointer = 0
        super().__init__(*args, **kwargs)
      
    def __set_pointer(self, cur_date):
        while self.get_row_at(self.pointer).DATE.dt.date.item() < cur_date:
            self.pointer += 1
    
    def __get_altered_sources(self, cur_ts, cur_date, cur_step_end, debug):
        local_pointer = self.pointer

        added, removed = [], []

        # Start at the first row with the date of `cur_date`
        cur_row = self.get_row_at(local_pointer)

        # Find the next rows that have the same date as `cur_date`
        while cur_row.DATE.dt.date.item() <= cur_date:

            # Add if the start of the manouvering falls in this timestep
            if cur_row.ETA.item()-MANOUVERING_TIME >= cur_ts and cur_row.ETA.item()-MANOUVERING_TIME < cur_step_end:
                # Source became active in this step
                added.append(
                    Ship(
                        cur_ts,
                        cur_row.SHIP.item(),
                        debug
                    )
                )
            
            # Remove if the time of departure falls in this timestep
            if cur_row.ETD.item() >= cur_ts and cur_row.ETD.item() < cur_step_end:
                # Source stopped being active this step
                removed.append(
                    Ship(
                        cur_ts,
                        cur_row.SHIP.item(),
                        debug
                    )
                )
            
            local_pointer += 1
            cur_row = self.get_row_at(local_pointer)
        
        if debug:
            self.__print_alterations(added, removed)
        
        return added, removed
    
    def __print_alterations(self, added, removed):
        def __print_list(name, lst):
            num = len(lst)
            if num > 0:
                print(f"{num} source{'s' if num > 1 else ''} {name}: {', '.join([source.name for source in lst])}")

        num_added, num_removed = len(added), len(removed)
        __print_list('added', added)
        __print_list('removed', removed)

    def parse_and_clean(self, df):
        '''
        Convert used times and dates to their respective formats and remove the rows that do not comply with specific types and formats.
        '''
        total_rows = len(df.index)

        # Parse the date and time columns to the datetime format
        df['DATE'] = pandas.to_datetime(df['DATE'], errors='coerce')
        df['ETA']  = pandas.to_datetime(df['ETA'], format='%H:%M', errors='coerce')
        df['ETD']  = pandas.to_datetime(df['ETD'], format='%H:%M', errors='coerce')
    
        # Drop the rows that do not have a valid date or time
        df = df.dropna(subset=['DATE'])
        df = df.dropna(subset=['ETA'])
        df = df.dropna(subset=['ETD'])

        # Add the date to times in order to cope with a timestep bigger than 1 day
        df['ETA'] = df.apply(lambda r : datetime.combine(r['DATE'], r['ETA'].time()), 1)
        df['ETD'] = df.apply(lambda r : datetime.combine(r['DATE'], r['ETD'].time()), 1)

        # Guarantee sorting on date column
        df = df.sort_values(by=['DATE'])
        
        # Count omitted rows
        new_total_rows = len(df.index)
        omitted_rows = new_total_rows - total_rows
        print(f'Omitted { -omitted_rows } rows due to unparsable dates and times. (= {round(omitted_rows / total_rows * 100, 2)}%)')
        print('____________________________________')
        print('')

        return df

    def update_sources(self, cur_ts, debug):
        cur_date, cur_step_end = cur_ts.date(), cur_ts + self.step

        # Move the pointer to the first entry starting with `cur_date`
        self.__set_pointer(cur_date)
        
        return self.__get_altered_sources(
            cur_ts,
            cur_date,
            cur_step_end,
            debug
        )  