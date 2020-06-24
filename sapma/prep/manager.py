from sapma.generic.managers.input import InputManager
from .handlers.properties import PropertyHandler

class Preparation:
    
    def __init__(self):
        InputManager(PropertyHandler())()
