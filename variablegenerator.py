__author__ = 'Synthetica'

class VariableGenerator(object):
    def __init__(self, name):
        self.name = name
        self.count = 0  # Updated to 1 at call

    def next(self):
        self.count += 1
        return '{name}_{count}'.format(name=self.name, count=self.count)
