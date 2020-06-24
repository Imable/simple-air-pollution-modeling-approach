class OutputManager:
    def __init__(self, handler):
        self.handler = handler

    def __call__(self, content):
        formatted_content = self.format(content)
        self.write_out(formatted_content)

    def format(self, content):
        return self.handler.format(content)
    
    def write_out(self, formatted_content):
        self.handler.write_out(formatted_content)