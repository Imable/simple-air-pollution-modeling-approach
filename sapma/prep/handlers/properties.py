from sapma.generic.static.properties import PROPERTIES
from os import path
from functools import reduce
from datetime import datetime, timedelta

class PropertyHandler:
    def __init__(self):
        self.base_options = {
            # Time options
            'T': [
                self.__make_option(
                    'start_ts',
                    parse=(lambda x: datetime.strptime(x, '%d-%m-%Y')),
                    mandatory=True),
                self.__make_option(
                    'end_ts', 
                    parse=(lambda x: datetime.strptime(x, '%d-%m-%Y')),
                    mandatory=True),
                self.__make_option(
                    'step', 
                    parse=(lambda x: timedelta(minutes=int(x))),
                    default=30)
            ], 
            # Data options
            'D': [
                self.__make_option(
                    'location', 
                    default='./sapma/input_files/'),
                self.__make_option(
                    'source_data', 
                    mandatory=True),
                self.__make_option(
                    'measurements', 
                    mandatory=True),
            ], 
            # Source options
            'S': [
                self.__make_option(
                    'placeholder')
            ], 
            # Layer options
            'L': [
                self.__make_option(
                    'placeholder')
            ], 
            # Miscellaneous
            'M': [
                self.__make_option(
                    'debug', 
                    parse=(lambda x: bool(x)),
                    default=False)
            ]
        }
    
    def __make_option(self, name, default=None, parse=lambda x: x, mandatory=False):
        return {
            'name':      name,
            'value':     parse(default) if default else None,
            'mandatory': mandatory,
            'parse':     parse
        }
    
    def __get_option(self, options, option_type, option_name):
        options_of_type = options[option_type]

        for option in options_of_type:
            if option['name'] == option_name:
                return option
        
        return None

    def __store_line(self, line, options):
        # Unpack the line by splitting on spaces
        option_type, option, value = line.split()
        options[option_type].append(self.__make_option(option, value))

    def __store_options(self, lines):
        options = {
            'T': [], 'D': [], 'S': [], 'L': [], 'M': []
        }

        for line in lines:
            self.__store_line(line, options)
        
        return options

    def __iterate(self, options):
        for option_type, options in options.items():
            for option in options:
                yield option_type, option

    def __backfill_defaults(self, options):
        def __check_mandatory(base_option, option):
            return not base_option['mandatory'] or option
        
        for option_type, base_option in self.__iterate(self.base_options):
            option = self.__get_option(options, option_type, base_option['name'])
            assert __check_mandatory(base_option, option)

            if not option:
                options[option_type].append(base_option)
            else:
                option['value'] = base_option['parse'](option['value'])

    def open(self):
        file = open(path.join(PROPERTIES.INPUT_DIR, PROPERTIES.INPUT_FILENAME))
        return file
    
    def read(self, file):
        def __valid(line):
            '''
            Skip spaces and comments starting with #
            '''
            return len(line.strip()) > 0 and not line[0] == '#'

        return reduce(lambda lines, line: lines + [line.strip()] if __valid(line) else lines, file.readlines(), [])
    
    def parse(self, lines):
        options = self.__store_options(lines)
        self.__backfill_defaults(options)

        return options
    
    def write_out(self, options):
        for _, option in self.__iterate(options):
            PROPERTIES.add(option)