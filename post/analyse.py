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
        else:
            self.dust_data.plot.area(
                x_compat=True,
                x='DATE',
                y=self.columns, 
                ax=ax,
                stacked=False)
        
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

        self.__date_format(ax)

        return ax
    
    def __plot_dust_modelcumsum(self, fig, grid, title):
        '''
        Plot raw measurements against cumulative sum of the model values and print the areas
        '''
        ax = fig.add_subplot(grid[0,:])
        ax.title.set_text(title)

        self.__add_dust_plot(ax, area=1)
        results_with_base = self.__add_model_cumsum(ax)

        self.__date_format(ax)

        area_model = numpy.trapz(results_with_base[self.model_col_name].cumsum().tolist())
        print(f'Model cumsum area {area_model}')

        area_values = {}
        for column in self.columns:
            if column != 'DATE':
                area_measurement = numpy.trapz(self.dust_data[column].tolist())
                area_values[column] = area_measurement
                print(f'Measurement area of {column}: {area_measurement}')

        for station, area in area_values.items():
            print(f'Lost particles at {station}: {area_model - area}')
            
        return ax
    
    def __plot_derivatives(self, fig, grid, title):
        '''
        Plot raw measurements against cumulative sum of the model values and print the areas
        '''
        ax = fig.add_subplot(grid[1,1])
        ax.title.set_text(title)

        print(self.results.values)

        derivatives = [
            pandas.Series(numpy.gradient(self.results.values), self.results.index, name=f'{self.model_col_name}_derivative')
        ]

        for column in self.columns:
            if column != 'DATE':
                derivatives.append(pandas.Series(numpy.gradient(self.dust_data[column].values), self.results.index, name=f'{column}_derivative'))

        return ax
        

    def plot(self):
        fig = plt.figure()
        grid = self.__get_grid()

        ax1 = self.__plot_dust_model_weather(fig, grid, 
            'Raw measurements against raw model')
        ax2 = self.__plot_dust_modelcumsum(fig, grid,
            'Raw measurements against cumulative sum of raw model')
        # ax3 = self.__plot_derivatives(fig, grid,
        #     'Derivatives of raw measurements and raw model')

        plt.show()