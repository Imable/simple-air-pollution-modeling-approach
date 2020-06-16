from datetime import datetime, timedelta
from tqdm import tqdm

class Loop:
    def __init__(self,
                start_ts, end_ts, step,
                func,
                debug):
        self.debug      = debug
        self.start_ts   = start_ts
        self.end_ts     = end_ts
        self.step       = step
        self.func       = func
        self.iterations = self.num_iter()

        if debug:
            print(f'Total iterations: { self.iterations }')

    def start(self):
        if self.debug:
            for i, cur_ts in self.timeframe():
                print(f'Iteration {i} - {cur_ts}')
                self.func(cur_ts, self.step)
        else:
            for i, cur_ts in tqdm(self.timeframe(), total=self.iterations):
                self.func(cur_ts, self.step)
        
    
    def timeframe(self):
        for iteration in range(self.iterations):
            elapsed = iteration * self.step
            yield iteration, self.start_ts + elapsed

    def num_iter(self):
        duration = self.end_ts - self.start_ts
        return int(duration / self.step)
    