class Analyse:
    def __init__(self, results):
        print('')
        # print(','.join([str(emissions) for ts, emissions in self.emissions.items()]))
        print(f'Cumulative emissions: {sum([emissions for ts, emissions in results.items()])}')