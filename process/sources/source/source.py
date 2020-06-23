class Source:
    def __init__(self, name, debug=False):
        self.debug     = debug
        self.name      = name
        self.emissions = {}

    def __eq__(self, other):
        return self.name == other.name
    
    def update(self, step, cur_ts, cur_step_end):
        self.emissions[cur_ts] = self.__emit(step, cur_ts)
    
    def gather_emissions(self, cur_ts):
        return self.emissions[cur_ts]

    def __emit(self, step, cur_ts):
        emissions = self.get_emissions(step, cur_ts)

        if self.debug and emissions > 0:
            print(f'{self.name} emitted {emissions}')

        return emissions

