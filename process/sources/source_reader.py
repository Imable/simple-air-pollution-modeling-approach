import pandas
from datetime import datetime

from .ship import Ship

BASE_PATH = './input'

class SourceReader:
    def __init__(self, fname, 
            start_ts, step):

        self.start_ts = start_ts
        self.step     = step
        self.data     = pandas.read_excel(self.__get_path(fname), header=1)

        # Row pointer that keeps track of the ships that have left the harbor
        self.pointer        = 0

        self.data = self.__parse_and_clean(self.data)

        # Remove the rows that precede the timeframe
        self.data = self.data[self.data['DATE'] >= start_ts]

    def __parse_and_clean(self, df):
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
    
    def __get_path(self, fname):
        return f'{ BASE_PATH }/{ fname }'
    
    def __set_pointer(self, cur_date):
        while self.__get_row_at(self.pointer).DATE.dt.date.item() < cur_date:
            self.pointer += 1
    
    def __get_row_at(self, position):
        return self.data.iloc[[position]]
    
    def __get_altered_sources(self, cur_ts, cur_date, cur_step_end, debug):
        local_pointer = self.pointer

        added, removed = [], []

        # Start at the first row with the date of `cur_date`
        cur_row = self.__get_row_at(local_pointer)

        # Find the next rows that have the same date as `cur_date`
        while cur_row.DATE.dt.date.item() <= cur_date:

            if cur_row.ETA.item() >= cur_ts and cur_row.ETA.item() < cur_step_end:
                # Source became active in this step
                added.append(
                    Ship(
                        cur_row.SHIP.item(),
                        debug
                    )
                )
                    
            if cur_row.ETD.item() >= cur_ts and cur_row.ETD.item() < cur_step_end:
                # Source stopped being active this step
                removed.append(
                    Ship(
                        cur_row.SHIP.item(),
                        debug
                    )
                )
            
            local_pointer += 1
            cur_row = self.__get_row_at(local_pointer)
        
        if debug:
            self.__print_alterations(added, removed)
        
        return added, removed
    
    def __print_alterations(self, added, removed):
        def __print_list(name, lst):
            num = len(lst)
            if num > 0:
                print(f"{num} sources {name}: {', '.join([source.name for source in lst])}")

        num_added, num_removed = len(added), len(removed)
        __print_list('added', added)
        __print_list('removed', removed)

    
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