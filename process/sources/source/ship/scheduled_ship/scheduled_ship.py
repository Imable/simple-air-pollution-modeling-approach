from .schedule import Schedule, MANOUVERING_TIME
from ..ship import Ship

class ScheduledShip(Ship):
    def __init__(self, schedule, name, debug):
        self.debug     = debug

        self.name      = name
        self.schedule  = Schedule(schedule)
        self.emissions = {}

        self.manouver  = False, None
        self.removed   = False
    
    def __get_state(self, step, cur_ts):
        '''
        Determine if the ship has arrived or has left
        '''
        state = self.schedule.get_state(step, cur_ts)

        if state:
            if state == 'arrival':
                self.manouver = True, cur_ts + MANOUVERING_TIME

            elif state == 'idle':
                self.manouver = False, None

            elif state == 'leaving':
                self.manouver = True, cur_ts + MANOUVERING_TIME
        print(f'HURTIGRUTEN: {self.manouver}')
        
        return state

    def update(self, step, cur_ts, cur_step_end):      
        super().update(step, cur_ts, cur_step_end)

        
    def get_emissions(self, step, cur_ts):
        state = self.__get_state(step, cur_ts)

        # Only calculate emissions if the ship is actually present
        emissions = super().get_emissions(step, cur_ts) if state else 0

        return emissions