from .schedule import Schedule
from ..ship import Ship

class ShipState():
    def __init__(self):
        # Manouvering, Present, Not present
        self.state = None

    def get_state(self):
        return self.state

class ScheduledShip(Ship):
    def __init__(self, schedule, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.schedule = Schedule(schedule)
        self.present  = False
        # Override manouver variable, because a scheduled ship is not always there
        self.manouver = False
    
    def __get_presence(self, step, cur_ts):
        '''
        Determine if the ship has arrived or has left
        '''
        new_presence = self.schedule.is_present(step, cur_ts)

        if self.present != new_presence:
            self.present != self.present
            self.manouver = True
        
        return new_presence
        
    def get_emissions(self, step, cur_ts):
        presence = self.__get_presence(step, cur_ts)

        # Only calculate emissions if the ship is actually present
        emissions = super().get_emissions(step, cur_ts) if self.present else 0

        self.present = presence

        return emissions