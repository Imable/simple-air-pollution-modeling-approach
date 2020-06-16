class BaseSource:
    def __init__(self, name, debug=False):
        self.debug     = debug

        self.name      = name
        self.added     = True
        self.removed   = False

    def __eq__(self, other):
        return self.name == other.name
    
    def emit(self, step):
        '''
        Function that returns the emissions of the source for this timestep
        '''
        emissions = 0

        # If the source has been added, add the addition penalty
        if self.added:
            emissions += self.add()
            self.added = False

        # If the source has been removed, add the removal penalty and stop
        if self.removed:
            emissions += self.remove()
        # Otherwise add the idle emissions
        else:
            emissions += self.idle(step)

        if self.debug:
            print(f'{self.name} emitted {emissions}')

        return emissions

    def add(self):
        pass

    def idle(self, step):
        pass

    def remove(self):
        pass
