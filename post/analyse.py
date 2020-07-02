from .measurements_reader import MeasurementsReader
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec

import numpy
import pandas

class Analyse:
    def __init__(self, 
        results,
        start_ts, end_ts, step,
        measurements_data,
        pm_type, station,
        weather_plot,
        base_concentration):

        print('____________________________________')
        print('')

        self.start_ts = start_ts
        self.end_ts   = end_ts
        self.step     = step

        self.pm_type            = pm_type
        self.base_concentration = base_concentration
        self.weather_plot       = weather_plot
        self.results            = results
        self.columns            = [f'{s}_{pm_type}' for s in station]
        self.model_col_name     = f'MODEL_{self.pm_type}'

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

    def __get_grid(self):
        return gridspec.GridSpec(2,2)
    
    def __inject_base_concentration(self, results):
        results.iloc[0, results.columns.get_loc(self.model_col_name)] += self.base_concentration
        return results
    
    def __date_format(self, ax):
        date_format = mdates.DateFormatter('%d-%m-%Y %H:%M')
        ax.xaxis.set_major_formatter(date_format)
    
    def __add_weater_plot(self, ax):
        '''
        Adds weather factor plot on the second Y axis
        '''
        ax2 = ax.twinx()
        self.weather_data.plot(
            y=self.weather_plot,
            ax=ax2,
            color='gray',
            ls='dashed')
        ax2.set_axisbelow(True)
        ax2.legend(loc='upper right')
    
    def __add_dust_plot(self, ax, area=0):
        if not area:
            self.dust_data.plot(
                x_compat=True,
                x='DATE',
                y=self.columns, 
                ax=ax)
            ax.set_ylabel(f'{self.pm_type} in \u03BCg/m3')
        else:
            self.dust_data.plot.area(
                x_compat=True,
                x='DATE',
                y=self.columns, 
                ax=ax,
                stacked=False)
            ax.set_ylabel(f'{self.pm_type} in \u03BCg/m3')
        
    def __add_model_plot(self, ax):
        self.results.plot(
            ax=ax)

    def __add_model_cumsum(self, ax):
        self.results_with_base = self.__inject_base_concentration(self.results.copy())
        self.results_with_base.cumsum().plot.area(
            ax=ax,
            stacked=False
        )
        return self.results_with_base
    
    def __plot_dust_model_weather(self, fig, grid, title):
        '''
        Main plot top stretching entire width showing raw model values against raw measurement values whether or not with one weather parameter
        '''
        ax = fig.add_subplot(grid[1,0])
        ax.title.set_text(title)

        self.__add_dust_plot(ax)
        self.__add_model_plot(ax)
        
        ax.legend(loc='upper left')
        
        if self.weather_plot:
            self.__add_weater_plot(ax)

        # self.__date_format(ax)

        return ax
    
    def __plot_dust_modelcumsum(self, fig, grid, title):
        '''
        Plot raw measurements against cumulative sum of the model values and print the areas
        '''
        ax = fig.add_subplot(grid[0,:])
        ax.title.set_text(title)

        self.__add_dust_plot(ax, area=1)
        self.results_with_base = self.__add_model_cumsum(ax)

        # self.__date_format(ax)
            
        return ax
    
    def __plot_derivatives(self, fig, grid, title):
        '''
        Plot raw measurements against cumulative sum of the model values and print the areas
        '''
        ax = fig.add_subplot(grid[1,1])
        ax.title.set_text(title)
        
        dust_data_diff = self.dust_data[['DATE']].copy()
        dust_data_diff[self.columns] = self.dust_data[self.columns].diff()
        dust_data_diff.plot(ax=ax, x='DATE', y=self.columns)
        
        results_diff = self.results.copy()
        results_diff[self.model_col_name] = self.results[self.model_col_name].diff()
        results_diff.plot(ax=ax)

        # self.__date_format(ax)

        return ax
    
    def __write_results(self):
        area_model = numpy.trapz(self.results_with_base[self.model_col_name].cumsum().tolist(), dx=self.step.total_seconds()/3600)

        area_values = {}
        for column in self.columns:
            if column != 'DATE':
                area_measurement = numpy.trapz(self.dust_data[column].tolist(), dx=self.step.total_seconds()/3600)
                area_values[column] = area_measurement

        print(f'Cumulative concentration in volume: {area_model} \u03BCg/m3')
        print(f'____________________________________')
        print('')

        num_hours = (self.end_ts - self.start_ts).total_seconds()/3600

        for station, area in area_values.items():
            print(f'{station}')
            print(f' > Accumulated hourly measured concentration: {area} \u03BCg/m3')
            print(f' > Difference between model estimation and {station}: {area_model} - {area} = {area_model - area} \u03BCg/m3')
            print(f' > Released concentration at {station} every hour: {(area_model - area)/num_hours} \u03BCg/m3')
            print(f'____________________________________')
            print('')

        
    def plot(self):
        fig = plt.figure()
        grid = self.__get_grid()

        ax1 = self.__plot_dust_model_weather(fig, grid, 
            'Raw measurements against raw model')
        ax2 = self.__plot_dust_modelcumsum(fig, grid,
            'Raw measurements against cumulative sum of raw model')
        ax3 = self.__plot_derivatives(fig, grid,
            'Derivatives of raw measurements and raw model')
        ax4 = self.__write_results()

        # uncomment to store results in a file
        # fig.savefig("results.pdf", bbox_inches='tight')
        fig.tight_layout()

        plt.show()