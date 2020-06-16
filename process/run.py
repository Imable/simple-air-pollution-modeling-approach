from .loop import Loop
from .sources.source_reader import SourceReader

class Run:
    def __init__(self, 
                start_ts, end_ts, step,
                source_data):

        self.source_data = SourceReader(
            source_data, 
            start_ts, step)
        
        loop = Loop(start_ts, end_ts, step, self.iteration)
        loop.start()
    
    def iteration(self, cur_ts):
        added, removed = self.source_data.update_sources(cur_ts)
        


        
