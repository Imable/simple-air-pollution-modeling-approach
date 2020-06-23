from .arguments import Arguments, ARGUMENTS
from .raster import Raster

class Init:
    def __init__(self):
        self.conf = Arguments().get()
        # self.conf['raster']        = Raster(self.conf['raster'])
        # self.conf['raster_volume'] = self.conf['raster'].get_volume(self.conf['inversion_layer'])

        self.print_conf()
    
    def get_conf(self):
        return self.conf
    
    def print_conf(self):
        print('')
        print('____________________________________')
        print('')
        print('Running model with the following configuration:')
        print('____________________________________')
        print('')
        for argument, props in ARGUMENTS.items():
            print(f'{ argument } : { self.conf[argument] }')
        print('____________________________________')
        print('')


