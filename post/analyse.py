from .measurements_reader import MeasurementsReader
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class Analyse:
    def __init__(self, 
        results,
        start_ts, end_ts, step,
        measurements_data,
        pm_type, station,
        weather_plot):

        self.pm_type = pm_type
        self.weather_plot = weather_plot

        self.results = results
        self.columns = [f'{s}_{pm_type}' for s in station]

        # Create Pandas dataframe from the measurements .xlsx file
        self.dust_data = MeasurementsReader(
            self.columns,
            self.pm_type,
            measurements_data,
            start_ts, end_ts, step,
            header_rows=0,
            sheet=1
        ).fetch()

        self.weather_data = MeasurementsReader(
            self.weather_plot,
            self.pm_type,
            measurements_data,
            start_ts, end_ts, step,
        ).fetch()

        self.plot()
    
    def __date_format(self, ax):
        date_format = mdates.DateFormatter('%d-%m-%Y %H:%M')
        ax.xaxis.set_major_formatter(date_format)
    
    def __add_weater_plot(self, ax):
        # ax.get_legend().remove()
        ax2 = ax.twinx()
        self.weather_data.plot(
            x='DATE',
            y=self.weather_plot,
            ax=ax2,
            color='gray',
            ls='dashed')
        ax2.set_axisbelow(True)
        ax2.legend(loc='upper right')

    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)

        self.dust_data.plot(
            x='DATE', 
            y=self.columns, 
            ax=ax)
        self.results.plot(
            ax=ax)
        
        ax.legend(loc='upper left')
        
        if self.weather_plot:
            self.__add_weater_plot(ax)

        self.__date_format(ax)
 
        plt.show()