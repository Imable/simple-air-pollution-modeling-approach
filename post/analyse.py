from .measurements_reader import MeasurementsReader
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec

import numpy
import pandas
import openpyxl
import math

class Analyse:
    def __init__(self, 
        results,
        start_ts, end_ts, step,
        measurements_data,
        pm_type, station,
        weather_plot,
        base_concentration,
        graphs):

        print('____________________________________')
        print('')

        self.export = {}

        self.start_ts = start_ts
        self.end_ts   = end_ts
        self.step     = step

        self.pm_type            = pm_type
        self.base_concentration = base_concentration
        self.weather_plot       = weather_plot
        self.results            = results
        self.columns            = [f'{s}_{pm_type}' for s in station]
        self.model_col_name     = f'MODEL_{self.pm_type}'
        # self.results_with_base_cumsum      = self.__inject_base_concentration_and_cumsum()
        self.results_with_base_raw_cumarea = self.__raw_area()

        self.export['Model concentration in system'] = self.results_with_base_raw_cumarea

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

        self.graph_def = [
            {
                'title': 'Raw model vs raw concentration measured',
                'f': self.__plot_dust_model_weather
            },
            {
                'title': 'Expected concentration (accumulated) vs real concentration (per m3) currently in system', 
                'f': self.__plot_dust_model_raw_area
            },
            {
                'title': 'Difference in concentration',
                'f': self.__plot_raw_difference
            },
            {
                'title': 'Difference in accumulated total concentration',
                'f': self.__plot_difference_modelcumsum_dust
            }
        ]
        self.graphs = graphs if graphs else [i for i in range(len(self.graph_def))]

        self.fig, self.grid = plt.figure(), self.__get_grid()

        self.plot()
        self.excel_export()
    
    def excel_export(self):
        writer = pandas.ExcelWriter('out.xlsx')

        for name, df in self.export.items():
            df.to_excel(writer, name)

        self.dust_data.set_index('DATE').to_excel(writer, 'DUST_DATA')
        self.weather_data.set_index('DATE').to_excel(writer, 'WEATHER_DATA')

        print('Done! See results in `out.xlsx`')
        
        writer.save()

    def __get_grid(self):
        return gridspec.GridSpec(math.ceil(len(self.graphs)/2), 1 if len(self.graphs) < 2 else 2)
    
    # def __inject_base_concentration_and_cumsum(self):
    #     results = self.results.copy()
    #     results.iloc[0, results.columns.get_loc(self.model_col_name)] += self.base_concentration
    #     results[self.model_col_name] = results[self.model_col_name].cumsum()
    #     results[self.model_col_name] = results[self.model_col_name].expanding().apply(lambda x: numpy.trapz(x.tolist(), dx=self.step.total_seconds()/3600))

    #     return results
    
    def __raw_area(self):
        results = self.results.copy()

        self.export['Values of non-accumulated sum'] = results[self.model_col_name]

        results.iloc[0, results.columns.get_loc(self.model_col_name)] += (self.base_concentration * 2)
        results[self.model_col_name] = results[self.model_col_name].expanding().apply(lambda x: numpy.trapz(x.tolist(), dx=self.step.total_seconds()/3600))
        return results
    
    def __date_format(self):
        return mdates.DateFormatter('%d-%m-%Y %H:%M')
    
    def __add_optional_weater_plot(self, ax):
        '''
        Adds weather factor plot on the second Y axis
        '''
       
        if self.weather_plot:
            ax2 = ax.twinx()
            ax.legend(loc='upper left')

            self.weather_data.plot(
                x_compat=True,
                x='DATE',
                y=self.weather_plot,
                ax=ax2,
                color='gray',
                ls='dashed')
            ax2.set_axisbelow(True)
            ax2.legend(loc='upper right')
    
    def __add_dust_plot(self, ax, area=0):
        if not area:
            self.dust_data.plot(
                x='DATE',
                y=self.columns, 
                x_compat=True,
                ax=ax)
            ax.set_ylabel(f'{self.pm_type} in \u03BCg/m3')
        else:
            self.dust_data.plot.area(
                x='DATE',
                y=self.columns, 
                ax=ax,
                x_compat=True,
                stacked=False)
            ax.set_ylabel(f'{self.pm_type} in \u03BCg/m3')
        
    def __add_model_plot(self, ax):
        self.results.reset_index().plot(
            x='index',
            y=self.model_col_name,
            ax=ax)
        ax.set_xlabel('DATE')

    def __add_model_cumsum_area(self, ax):
        self.results_with_base_cumsum.reset_index().plot.area(
            x='index',
            y=self.model_col_name,
            ax=ax,
            stacked=False
        )
        ax.set_xlabel('DATE')
    
    def __add_model_raw_area(self, ax):
        self.results_with_base_raw_cumarea.reset_index().plot.area(
            x='index',
            y=self.model_col_name,
            ax=ax,
            stacked=False
        )
        ax.set_xlabel('DATE')
    
    def __plot_dust_model_weather(self, ax):
        '''
        Main plot top stretching entire width showing raw model values against raw measurement values whether or not with one weather parameter
        '''

        self.__add_dust_plot(ax)
        self.__add_model_plot(ax)

        self.__add_optional_weater_plot(ax)
        
        return ax
    
    def __plot_dust_model_raw_area(self, ax):
        '''
        Plot raw measurements against cumulative sum of the model values and print the areas
        '''

        self.__add_dust_plot(ax, area=1)
        self.__add_model_raw_area(ax)      
        self.__add_optional_weater_plot(ax)

        return ax
    
    def __plot_derivatives(self):
        '''
        Plot raw measurements against cumulative sum of the model values and print the areas
        '''

        dust_data_diff = self.dust_data[['DATE']].copy()
        dust_data_diff[self.columns] = self.dust_data[self.columns].diff()
        dust_data_diff.plot(ax=ax, x='DATE', y=self.columns)
        
        results_diff = self.results.copy()
        results_diff[self.model_col_name] = self.results[self.model_col_name].diff()
        results_diff.plot(ax=ax)

        # self.__date_format(ax)

        return ax
    
    def __plot_difference_modelcumsum_dust(self, ax):
        tmp = self.dust_data.copy()
        # From expected concentration per hour to expected concentration from start_ts until now
        tmp[self.model_col_name] = self.results_with_base_raw_cumarea.reset_index()[self.model_col_name].expanding().apply(lambda x: numpy.trapz(x.tolist(), dx=self.step.total_seconds()/3600))
        diff_columns = []

        for column in self.columns:
            diff_column = f'diff_{column}'
            diff_columns.append(diff_column)
            # From expected concentration per hour to expected concentration from start_ts until now
            tmp[column] = tmp[column].expanding().apply(lambda x: numpy.trapz(x.tolist(), dx=self.step.total_seconds()/3600))
            tmp[diff_column] = tmp[self.model_col_name] - tmp[column]
        
        tmp.plot(
            x='DATE',
            y=diff_columns, 
            ax=ax,
            x_compat=True)
        ax.set_ylabel(f'{self.pm_type} in \u03BCg/m3')

        self.__add_optional_weater_plot(ax)

    def __plot_raw_difference(self, ax):
        tmp = self.dust_data.copy()

        diff_columns = []

        for column in self.columns:
            diff_column = f'diff_{column}'
            diff_columns.append(diff_column)
            tmp[diff_column] = self.results_with_base_raw_cumarea.reset_index()[self.model_col_name] - tmp[column]

        self.export['Difference in concentration'] = tmp.set_index('DATE')[diff_columns]
        
        tmp.plot(
            x='DATE',
            y=diff_columns, 
            ax=ax,
            x_compat=True)
        ax.set_ylabel(f'{self.pm_type} in \u03BCg/m3')

        self.__add_optional_weater_plot(ax)
        
    
    def __write_results(self):
        area_model = numpy.trapz(self.results_with_base_raw_cumarea[self.model_col_name].tolist(), dx=self.step.total_seconds()/3600)

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
            print(f' > Accumulated measured concentration: {area} \u03BCg/m3')
            print(f' > Difference between model estimation and {station}: {area_model} - {area} = {area_model - area} \u03BCg/m3')
            # print(f' > Released concentration at {station} every hour: {(area_model - area)/num_hours} \u03BCg/m3')
            print(f'____________________________________')
            print('')
    
    def __plot(self, pos, title, func):
        ax = self.fig.add_subplot(self.grid[pos])
        ax.xaxis.set_major_formatter(self.__date_format())
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.title.set_text(title)
        func(ax)
        
    def plot(self):
        actual_i = 0
        for i, graph in enumerate(self.graph_def):
            if i in self.graphs:
                pos = (math.floor(actual_i / 2), actual_i % 2)
                self.__plot(pos, graph['title'], graph['f'])
                actual_i += 1

        self.__write_results()

        print('Close the plot window to store the results in an Excel sheet...')
        print('____________________________________')
        print('')

        # ax1 = self.__plot_dust_model_weather(fig, grid, 
        #     'Raw measurements against raw model')
        # ax2 = self.__plot_dust_modelcumsum(fig, grid,
        #     'Raw measurements against cumulative sum of raw model')
        # ax3 = self.__plot_derivatives(fig, grid,
        #     'Derivatives of raw measurements and raw model')
        # ax5 = self.__plot_difference_modelcumsum_dust(fig, grid,
        #     'Difference between cumulative model and raw measurements')

        # uncomment to store results in a file
        # self.fig.savefig("results.pdf", bbox_inches='tight')
        self.fig.tight_layout()

        plt.show()