class BaseSource:
    def __init__(self, name):
        self.name      = name
        self.added     = True
        self.removed   = False
        self.emissions = 0

    def __eq__(self, other):
        return self.name == other.name
    
    def emit(self, step):
        '''
        Function that returns the emissions of the source for this timestep
        '''
        new_emissions = 0

        if self.added:
            new_emissions += self.add()
            self.added = False

        if self.removed:
            new_emissions += self.remove()
            self.removed = True
        
        new_emissions += self.idle(step)

        self.emissions += new_emissions
        print(f'{self.name} emitted {new_emissions}')
        return self.emissions

    def add(self):
        pass

    def idle(self, step):
        pass

    def remove(self):
        pass
