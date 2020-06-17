from .measurements_reader import MeasurementsReader

class Analyse:
    def __init__(self, 
        results,
        start_ts, end_ts, step,
        measurements_data):

        self.measurements_data = MeasurementsReader(
            measurements_data,
            start_ts, end_ts, step,
            0
        )

        print('')
        # print(','.join([str(emissions) for ts, emissions in self.emissions.items()]))
        print(f'Cumulative emissions: {sum([emissions for ts, emissions in results.items()])}')