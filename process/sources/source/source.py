class Source:
    def __init__(self, name, debug=False):
        self.debug     = debug
        self.name      = name

    def __eq__(self, other):
        return self.name == other.name

    def emit(self, step, cur_ts):
        emissions = self.get_emissions(step, cur_ts)

        if self.debug and emissions > 0:
            print(f'{self.name} emitted {emissions}')

        return emissions

