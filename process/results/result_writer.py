import pandas

class ResultWriter:

    def __init__(self, pm_type):
        self.pm_type   = pm_type
        # Format = {'datetime': [pm_value] }
        self.emissions = {}
    
    def append(self, cur_ts, result):
        self.emissions[cur_ts] = [result]
    
    def get(self):
        return pandas.DataFrame.from_dict(
            self.emissions, 
            orient='index',
            columns=[self.pm_type])