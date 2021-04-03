import pandas

class ResultWriter:

    def __init__(self, step, pm_type):
        self.step    = step
        self.pm_type = pm_type

        # Format = {'datetime': [pm_value] }
        self.emissions    = {}
        # self.contributors = {}
    
    def append_emissions(self, cur_ts, result, contributors):
        self.emissions[cur_ts] = ([result], contributors)
    
    # def append_contributors(self, cur_ts, contributors):
    #     self.contributors[cur_ts] = contributors
    
    def get(self):
        new_emissions = {}

        # Concatenate per hour to match the resolution of the measurements
        for date, (value, contributors) in self.emissions.items():
            key = date.replace(minute=0, second=0)

            if key in new_emissions:
                new_emissions[key] = (new_emissions[key][0] + sum(value), new_emissions[key][1] + contributors)
            else:
                new_emissions[key] = (sum(value), contributors)

            # Remove duplicate contributors
            new_emissions[key] = (new_emissions[key][0], list(set(new_emissions[key][1])))

        return pandas.DataFrame.from_dict(
            new_emissions, 
            orient='index',
            columns=[f'MODEL_{self.pm_type}', 'CONTRIBUTORS'])