from .base_source import BaseSource

class Ship(BaseSource):

    def add(self):
        self.emissions += 10

    def idle(self):
        pass

    def remove(self):
        pass