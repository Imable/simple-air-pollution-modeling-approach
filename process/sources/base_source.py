class BaseSource:
    def __init__(self, name):
        self.name      = name
        self.emissions = 0

    def __eq__(self, other):
        return self.name == other.name

    def add(self):
        pass

    def idle(self):
        pass

    def remove(self):
        pass
