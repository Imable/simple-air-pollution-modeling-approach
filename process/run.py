from .loop import Loop

class Run:
    def __init__(self, 
                start_ts, end_ts, step):
        # TODO: Read data sources
        # TODO: Start the loop with iteration()
        loop = Loop(start_ts, end_ts, step, self.iteration)
        loop.start()
    
    def iteration(self, cur_ts):
        print(cur_ts)

        
