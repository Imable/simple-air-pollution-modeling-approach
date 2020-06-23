from .volume import Volume

class Layers:

    def __init__(self, inversion_layer_height):
        self.inversion_layer_height = inversion_layer_height

    def get_current_volume(self):
        return Volume.get_volume(self.inversion_layer_height)