from ..source import Source
from ...pm_formula.formula_manager import FormulaManager
from datetime import timedelta

class Ship(Source):

    def __init__(self, cur_ts, manouvering_time, *args, **kwargs):
        self.manouvering_time = manouvering_time
        self.manouver  = True, cur_ts + self.manouvering_time
        self.removed   = False

        super().__init__(*args, **kwargs)

        self.formula   = FormulaManager(self.name)

    def update(self, step, cur_ts, cur_step_end):      
        super().update(step, cur_ts, cur_step_end)

        # If the ship is manouvering now and the end of its manouvering is in this timeframe, stop manouvering the next timestep
        if self.manouver[0] and self.manouver[1] <= cur_step_end:
            self.manouver = False, None

    def remove(self, cur_ts):
        self.manouver = True, cur_ts + self.manouvering_time
        self.removed  = True
    
    def can_be_removed(self):
        return not self.manouver[0] and self.removed

    def manouvering(self, step):
        return self.formula.get_manouvering() * (step.total_seconds() / 60)

    def idle(self, step):
        return self.formula.get_idle() * (step.total_seconds() / 60)

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