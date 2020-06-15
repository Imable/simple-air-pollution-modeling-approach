import argparse
from datetime import datetime

ARGUMENTS = {
    'start_ts': {
        'help': 'Date of the start of calculation timeframe in DD-MM-YYYY format',
        'parse': (lambda x: datetime.strptime(x, '%d-%m-%Y'))
    },
    'end_ts': {
        'help': 'Date of the end of calculation timeframe in DD-MM-YYYY format',
        'parse': (lambda x: datetime.strptime(x, '%d-%m-%Y')) 
    },
    'step': {
        'help': 'Step size for the model interval in minutes (M)',
        'parse': (lambda x: int(x))  
    },
    'raster': {
        'help': 'Filepath of the file containing the digital elevation model',
        'parse': (lambda x: x)
    },
    'inversion_layer': {
        'help': 'Inversion layer height in meters (m)',
        'parse': (lambda x: int(x))
    }
    # 'validation_data': 'Filepath of a file including own measured concentration data in CSV format',
    # 'source_data': 'Filepath of a file including data of pollution sources',
}

# Read the input arguments. They will be accessible through `arguments.[argument name here]`
class Arguments():
    def __init__(self):
        self.reader = argparse.ArgumentParser()

        for tag, props in ARGUMENTS.items():
            self.add(tag, props['help'])

    def add(self, tag, help):
        self.reader.add_argument(f'--{tag}', help=help)

    def get(self):
        args = vars(self.reader.parse_args())
        return self.parse_args_to_type(args)
    
    def parse_args_to_type(self, args):
        args_parsed_to_type = {}

        for tag, props in ARGUMENTS.items():
            args_parsed_to_type[tag] = props['parse'](args[tag])
        
        return args_parsed_to_type
        
        
        