from os import path

class Properties:
    def __init__(self):
        self.ROOT_DIR = path.abspath(path.join(path.dirname(__file__), '../..'))
        self.INPUT_DIR = path.join(self.ROOT_DIR, 'input_files')
        self.INPUT_FILENAME = 'sapma.inp'
    
    def add(self, option):
        self.__dict__[option['name']] = option['value'] 

    # @property
    # def BASE_PATH(self):
    #     return self.__BASE_PATH
    
    # @BASE_PATH.setter
    # def BASE_PATH(self, base_path):
    #     self._BASE_PATH = base_path
    
    # @property
    # def INPUT_FILENAME(self):
    #     return self._INPUT_FILENAME

    # @BASE_PATH.setter
    # def INPUT_FILENAME(self, input_filename):
    #     self._INPUT_FILENAME = input_filename

PROPERTIES = Properties()