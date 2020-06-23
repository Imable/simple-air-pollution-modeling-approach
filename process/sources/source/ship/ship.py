from ..source import Source
from datetime import timedelta

MANOUVERING_TIME = timedelta(minutes=30)

class Ship(Source):

    def __init__(self, cur_ts, *args, **kwargs):
        self.manouver  = True, cur_ts + MANOUVERING_TIME
        self.removed   = False

        super().__init__(*args, **kwargs)

    def update(self, step, cur_ts, cur_step_end):      
        super().update(step, cur_ts, cur_step_end)

        # If the ship is manouvering now and the end of its manouvering is in this timeframe, stop manouvering the next timestep
        if self.manouver[0] and self.manouver[1] <= cur_step_end:
            self.manouver = False, None

    def remove(self, cur_ts):
        self.manouver = True, cur_ts + MANOUVERING_TIME
        self.removed  = True
    
    def can_be_removed(self):
        return not self.manouver[0] and self.removed

    def manouvering(self, step):
        return 0.05 * (step.total_seconds() / 60)

    def idle(self, step):
        # Addition per minute
        return 0.001 * (step.total_seconds() / 60)

    def get_emissions(self, step, cur_ts):
        '''
        Function that returns the emissions of the source for this timestep
        '''
        emissions = 0

        if self.manouver[0]:
            emissions += self.manouvering(step)
        else:
            emissions += self.idle(step)
        
        return emissions