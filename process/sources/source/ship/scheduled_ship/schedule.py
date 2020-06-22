from datetime import datetime

class Schedule:
    def __init__(self, schedule):
        self.pointer  = 0 
        self.schedule = self.__parse_schedule(schedule)

    def __parse_date(self, date_string):
        return datetime.strptime(date_string, '%d-%m-%Y').date()

    def __parse_time(self, time_string):
        return datetime.strptime(time_string, '%H:%M').time()

    def __parse_schedule(self, raw_schedule):
        schedule = {}

        for date_range, dep_times in raw_schedule.items():
            p_date_range = tuple(self.__parse_date(date) for date in date_range)
            p_dep_times  = [self.__parse_time(time) for time in dep_times]
            schedule[p_date_range] = p_dep_times
            
        return schedule

    def __get_schedule(self):
        key = list(self.schedule.keys())[self.pointer]
        return key, self.schedule[key]

    def __set_pointer(self, cur_ts):
        '''
        Sets the pointer to point to the schedule entry that is valid either on or after the current date
        '''
        while cur_ts.date() < self.__get_schedule()[0][0]:
            self.pointer += 1
            
    def is_present(self, step, cur_ts):
        self.__set_pointer(cur_ts)
        _, times = self.__get_schedule()
        cur_time, cur_step_end = cur_ts.time(), (cur_ts + step).time()
        
        # If a time in the schedule exists that is in this current timestep, return true
        return any(map(lambda time: cur_time <= time < cur_step_end, times))
