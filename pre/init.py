from .arguments import Arguments, ARGUMENTS

class Init:
    def __init__(self):
        self.conf = Arguments().get()

        self.print_conf()
    
    def get_conf(self):
        return self.conf
    
    def print_conf(self):
        print('')
        print('____________________________________')
        print('')
        print('Running model with the following configuration:')
        print('____________________________________')
        print('')
        for argument, props in ARGUMENTS.items():
            print(f'{ argument } : { self.conf[argument] }')
        print('____________________________________')
        print('')


