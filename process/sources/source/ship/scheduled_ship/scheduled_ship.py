from .schedule import Schedule
from ..ship import Ship
from datetime import timedelta

class ScheduledShip(Ship):
    def __init__(self, schedule, harbour_time=timedelta(minutes=20), *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.schedule  = Schedule(schedule, self.manouvering_time, harbour_time)
        self.manouver  = False, None
    
    def __get_state(self, step, cur_ts):
        '''
        Determine if the ship has arrived or has left
        '''
        state = self.schedule.get_state(step, cur_ts)

        if state:
            if state == 'arrival':
                self.manouver = True, cur_ts + self.manouvering_time

            elif state == 'idle':
                self.manouver = False, None

            elif state == 'leaving':
                self.manouver = True, cur_ts + self.manouvering_time
        
        return state

    def update(self, step, cur_ts, cur_step_end):      
        super().update(step, cur_ts, cur_step_end)

        
    def get_emissions(self, step, cur_ts):
        state = self.__get_state(step, cur_ts)

        # Only calculate emissions if the ship is actually present
        emissions = super().get_emissions(step, cur_ts) if state else 0

        return emissions