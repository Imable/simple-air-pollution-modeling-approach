from datetime import datetime, timedelta

class Loop:
    def __init__(self,
                start_ts, end_ts, step,
                func):
        self.start_ts   = start_ts
        self.end_ts     = end_ts
        self.step       = step
        self.func       = func
        self.iterations = self.num_iter()

        print(f'Total iterations: { self.iterations }')

    def start(self):
        for cur_ts in self.timeframe():
            self.func(cur_ts)
    
    def timeframe(self):
        for iteration in range(self.iterations):
            elapsed = iteration * self.step
            yield self.start_ts + timedelta(minutes=elapsed)

    def num_iter(self):
        duration = self.end_ts - self.start_ts
        return int(duration / timedelta(minutes=self.step))
    