import argparse
import json
from datetime import datetime, timedelta

SHIP_SPECIFIC_DATA = None

ARGUMENTS = {
    'start_ts': {
        'help': 'Date of the start of calculation timeframe in DD-MM-YYYY format',
        'parse': (lambda x: datetime.strptime(x, '%d-%m-%Y')),
        'default': 'No start date provided'
    },
    'end_ts': {
        'help': 'Date of the end of calculation timeframe in DD-MM-YYYY format',
        'parse': (lambda x: datetime.strptime(x, '%d-%m-%Y')),
        'default': 'No end date provided'
    },
    'step': {
        'help': 'Step size for the model interval in minutes (M)',
        'parse': (lambda x: timedelta(minutes=int(x))),
        'default': '20'
    },
    'inversion_layer': {
        'help': 'Inversion layer height in meters (m)',
        'parse': (lambda x: int(x)),
        'default': 1800
    },
    'source_data': {
        'help': 'Filename of the .xlsx file containing source data',
        'parse': (lambda x: x),
        'default': None
    },
    'measurements_data': {
        'help': 'Filename of the .xlsx file containing your own measurements',
        'parse': (lambda x: x),
        'default': None
    },
    'pm_type': {
        'help': 'Type of PM that will be modelled',
        'parse': (lambda x: x),
        'default': 'PM2.5'
    },
    'station': {
        'help': 'Station of which the measurements will be plotted (G/C/D). Enter as: \'[\\"C\\", \\"D\\"]\'',
        'parse': (lambda x: json.loads(x)),
        'default': '["G"]'
    },
    'weather_plot': {
        'help': 'Column of the weather data that you want to plot as well. Enter as: \'[\\"G_T\\"]\'. If omitted, nothing will be plotted on the second axis.',
        'parse': (lambda x: json.loads(x)),
        'default': '[]'
    },
    'base_concentration': {
        'help': 'The concentration that is in the air of the model at the starting point.',
        'parse': lambda x: float(x),
        'default': 0
    },
    'graphs': {
        'help': 'The indices of the graphs that you want to show.  Enter as: \'[1, 2]\'. Leave empty to show all.',
        'parse': (lambda x: json.loads(x)),
        'default': 'null'
    },
    'debug': {
        'help': 'Show debug messages (will be slower)',
        'parse': (lambda x: bool(x)),
        'default': 0
    }
    # 'validation_data': 'Filepath of a file including own measured concentration data in CSV format',
    # 'source_data': 'Filepath of a file including data of pollution sources',
}

# Read the input arguments. They will be accessible through `arguments.[argument name here]`
class Arguments():
    def __init__(self):
        self.reader = argparse.ArgumentParser()

        for tag, props in ARGUMENTS.items():
            self.add(tag, props['help'], props['default'])

    def add(self, tag, help, default):
        self.reader.add_argument(f'--{tag}', help=help, default=default)

    def get(self):
        args = vars(self.reader.parse_args())
        return self.parse_args_to_type(args)
    
    def parse_args_to_type(self, args):
        args_parsed_to_type = {}

        for tag, props in ARGUMENTS.items():
            args_parsed_to_type[tag] = props['parse'](args[tag])
        
        return args_parsed_to_type
        