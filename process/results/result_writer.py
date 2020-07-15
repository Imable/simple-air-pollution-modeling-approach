import pandas

class ResultWriter:

    def __init__(self, step, pm_type):
        self.step    = step
        self.pm_type = pm_type

        # Format = {'datetime': [pm_value] }
        self.emissions = {}
    
    def append(self, cur_ts, result):
        self.emissions[cur_ts] = [result]
    
    def get(self):
        new_emissions = {}

        # Concatenate per hour to match the resolution of the measurements
        for date, value in self.emissions.items():
            key = date.replace(minute=0, second=0)

            if key in new_emissions:
                new_emissions[key] += sum(value)
            else:
                new_emissions[key] = sum(value)

        return pandas.DataFrame.from_dict(
            new_emissions, 
            orient='index',
            columns=[f'MODEL_{self.pm_type}'])