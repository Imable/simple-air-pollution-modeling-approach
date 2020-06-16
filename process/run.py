from .loop import Loop
from .sources.source_reader import SourceReader
from .results.result_writer import ResultWriter

class Run:
    def __init__(self, 
                start_ts, end_ts, step,
                source_data):

        self.source_data = SourceReader(
            source_data, 
            start_ts, step)

        self.active_sources = []
        
        loop = Loop(start_ts, end_ts, step, self.iteration)
        loop.start()

    def __fetch_new_sources(self, cur_ts):
        added, removed = self.source_data.update_sources(cur_ts)
        self.active_sources = [source for source in self.active_sources + added if source not in removed]
    
    def iteration(self, cur_ts):
        self.__fetch_new_sources(cur_ts)
        # print(self.active_sources)




        
