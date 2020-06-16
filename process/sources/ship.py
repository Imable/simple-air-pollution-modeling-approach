from .base_source import BaseSource

class Ship(BaseSource):

    def add(self):
        return 10

    def idle(self, step):
        return 0.1 * (step.total_seconds() / 60)

    def remove(self):
        return 10