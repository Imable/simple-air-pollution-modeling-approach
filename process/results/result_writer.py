class ResultWriter:

    def __init__(self):
        self.emissions = {}
    
    def append(self, cur_ts, result):
        self.emissions[cur_ts] = result
    
    def get(self):
        return self.emissions