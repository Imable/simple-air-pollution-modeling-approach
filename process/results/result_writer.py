class ResultWriter:

    def __init__(self):
        self.emissions = {}
    
    def append(self, cur_ts, result):
        self.emissions[cur_ts] = result
    
    def show_results(self):
        print('')
        # print(','.join([str(emissions) for ts, emissions in self.emissions.items()]))
        print(f'Cumulative emissions: {sum([emissions for ts, emissions in self.emissions.items()])}')