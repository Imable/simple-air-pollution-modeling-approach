from .loop import Loop
from .sources.input.source_reader import SourceReader
from .results.result_writer import ResultWriter
from .sources.source.source_factory import SourceFactory
from .layers.layers import Layers

class Model:
    def __init__(self, 
                start_ts, end_ts, step,
                source_data,
                inversion_layer,
                pm_type,
                debug):
        self.debug    = debug

        self.start_ts = start_ts
        self.end_ts   = end_ts
        self.step     = step

        self.source_data = SourceReader(
            source_data, 
            start_ts, end_ts, step,
            mask=0,
            header_rows=1
        )

        self.active_sources = SourceFactory.get_initial_sources(debug)

        self.layers  = Layers(inversion_layer)
        self.results = ResultWriter(step, pm_type)
        
    def __remove_old_sources(self):
        # Only keep sources that have not been removed
        self.active_sources = [source for source in self.active_sources if not source.can_be_removed()]

    def __update_sources(self, cur_ts):
        # Fetch the altered sources from the sheet
        added, removed = self.source_data.update_sources(cur_ts, self.debug)

        # Add the new sources to the active sources list
        self.active_sources += added

        # Flag the removed sources as removed, such that we can calculate their removal penalty and remove them before the next iteration
        for source in removed:
            index = self.active_sources.index(source)
            self.active_sources[index].remove(cur_ts)

    def __combine_emissions(self, cur_ts, step):
        emissions = 0
        names     = []

        for source in self.active_sources:
            source.update(step, cur_ts, cur_ts+step)
            emissions += source.gather_emissions(cur_ts)

            # Gather the names of the sources contributing to these emissions
            # 'if' in order to not add ships when they don't emit anything (e.g. ferry)
            if emissions > 0:
                names.append(source.name)

        return emissions, names
    
    def __calculate_concentration(self, emissions):
        volume = self.layers.get_current_volume()
        return emissions / volume
    
    def run(self):
        loop = Loop(
            self.start_ts, 
            self.end_ts, 
            self.step, 
            self.iteration, 
            self.debug
        )
        loop.start()

        return self.results.get()

    def iteration(self, cur_ts, step):
        self.__remove_old_sources()
        self.__update_sources(cur_ts)
        emissions, names = self.__combine_emissions(cur_ts, step)
        concentration    = self.__calculate_concentration(emissions)

        self.results.append_emissions(cur_ts, concentration, names)

        # Store the name of sources contributing to this timesteps' emissions
        # self.results.append_contributors(cur_ts, names)
