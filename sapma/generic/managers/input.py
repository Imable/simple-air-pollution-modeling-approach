class InputManager:

    def __init__(self, handler):
        self.handler = handler
    
    def __call__(self):
        file           = self.open()
        content        = self.read(file)
        parsed_content = self.parse(content)
        return self.write_out(parsed_content)

    def open(self):
        return self.handler.open()
    
    def read(self, file):
        return self.handler.read(file)
    
    def parse(self, content):
        return self.handler.parse(content)
    
    def write_out(self, parsed_content):
        return self.handler.write_out(parsed_content)