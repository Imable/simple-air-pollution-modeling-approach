from .arguments import Arguments
from .raster import Raster

class Init:
    def __init__(self):
        self.conf = Arguments().get()
        self.conf['raster']        = Raster(self.conf['raster'])
        self.conf['raster_volume'] = self.conf['raster'].get_volume(self.conf['inversion_layer'])
    
    def get_conf(self):
        return self.conf

