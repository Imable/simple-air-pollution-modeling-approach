from .measurements_reader import MeasurementsReader
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class Analyse:
    def __init__(self, 
        results,
        start_ts, end_ts, step,
        measurements_data,
        pm_type, station):

        self.results = results
        self.columns = [f'{s}_{pm_type}' for s in station]

        # Create Pandas dataframe from the measurements .xlsx file
        self.measurements_data = MeasurementsReader(
            self.columns,
            measurements_data,
            start_ts, end_ts, step,
            0
        ).fetch()

        self.plot()

        # print('')
        # print(','.join([str(emissions) for ts, emissions in self.emissions.items()]))
        # print(f'Cumulative emissions: {sum([emissions for ts, emissions in results.items()])}')
    
    def __date_format(self, ax):
        date_format = mdates.DateFormatter('%d-%m-%Y %H:%M')
        ax.xaxis.set_major_formatter(date_format)

    def plot(self):
        ax = self.measurements_data.plot(
            x='DATE',
            y=self.columns,
            kind='line'
        )
        self.results.plot(ax=ax)
        self.__date_format(ax)
 
        plt.show()