from .loop import Loop
from .sources.source_reader import SourceReader
from .results.result_writer import ResultWriter

class Run:
    def __init__(self, 
                start_ts, end_ts, step,
                source_data,
                debug):
        self.debug = debug

        self.source_data = SourceReader(
            source_data, 
            start_ts, step)

        self.active_sources = []

        self.results = ResultWriter()
        
        loop = Loop(start_ts, end_ts, step, self.iteration, debug)
        loop.start()

        self.results.show_results()

    def __remove_old_sources(self):
        # Only keep sources that have not been removed
        self.active_sources = [source for source in self.active_sources if not source.removed]

    def __update_sources(self, cur_ts):
        # Fetch the altered sources from the sheet
        added, removed = self.source_data.update_sources(cur_ts, self.debug)

        # Add the new sources to the active sources list
        self.active_sources += added

        # Flag the removed sources as removed, such that we can calculate their removal penalty and remove them before the next iteration
        for source in removed:
            index = self.active_sources.index(source)
            self.active_sources[index].removed = True

    def __combine_emissions(self, cur_ts, step):
        emissions = 0

        for source in self.active_sources:
            emissions += source.emit(step)
        
        return emissions

    def iteration(self, cur_ts, step):
        self.__remove_old_sources()
        self.__update_sources(cur_ts)
        emissions = self.__combine_emissions(cur_ts, step)
        self.results.append(cur_ts, emissions)





        
