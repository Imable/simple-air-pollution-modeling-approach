from ..source import Source

class Ship(Source):

    def __init__(self, *args, **kwargs):
        self.manouver  = True
        self.removed   = False

        super().__init__(*args, **kwargs)

    def remove(self):
        self.manouver = True
        self.removed  = True

    def manouvering(self):
        return 0.02

    def idle(self, step):
        # Addition per minute
        return 0.001 * (step.total_seconds() / 60)

    def get_emissions(self, step, cur_ts):
        '''
        Function that returns the emissions of the source for this timestep
        '''
        emissions = 0

        # If the source has been added, add the addition penalty
        if self.manouver:
            emissions += self.manouvering()
            self.manouver = False

        # If the source has been removed, add the removal penalty and stop
        if not self.removed:
            emissions += self.idle(step)
        
        return emissions