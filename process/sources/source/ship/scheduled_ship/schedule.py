from datetime import date, datetime, timedelta

class Schedule:
    def __init__(self, schedule, manouvering_time=timedelta(minutes=20), harbour_time=timedelta(minutes=20)):
        self.manouvering_time = manouvering_time
        self.harbour_time = harbour_time
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
    
    def __time_calc(self, time, delta, operator):
        res = None

        if operator == '+':
            res = datetime.combine(date.today(), time) + delta
        else:
            res = datetime.combine(date.today(), time) - delta

        return res.time()
    
    def __make_interval(self, time):
        start_arrival = self.__time_calc(time, self.manouvering_time, '-') 
        start_idle    = time
        start_leaving = self.__time_calc(time, self.harbour_time, '+')

        return start_arrival, start_idle, start_leaving

    def __set_pointer(self, cur_ts):
        '''
        Sets the pointer to point to the schedule entry that is valid either on or after the current date
        '''
        while self.pointer < len(self.schedule) and self.__get_schedule()[0][1] < cur_ts.date():
            self.pointer += 1
            
    def get_state(self, step, cur_ts):
        self.__set_pointer(cur_ts)
        dates, times = self.__get_schedule()
        cur_time, cur_step_end = cur_ts.time(), (cur_ts + step).time()

        state = None

        if dates[0] <= cur_ts.date() <= dates[1]:

            for time in times:
                arrival, idle, leave = self.__make_interval(time)

                if cur_time >= arrival and cur_time < idle:
                    state = 'arrival'
                elif cur_time >= idle and cur_time < leave:
                    state = 'idle'
                elif cur_time >= leave and cur_time < self.__time_calc(leave, self.manouvering_time, '+'):
                    state = 'leaving'
                
                if state:
                    break
        
        return state
