from trace import Trace
import importlib
from driver import *

class GenerateSequenceDiagram:
    def __init__(self, driver_module):
        self.driver_module = __import__(driver_module)

    def get_called_functions(self, driver_function):
        self.driver_function = getattr(self.driver_module, driver_function)
        self.driver_function()
        # print(dir(self.driver_function))
        # print(self.driver_function.__name__)
        tracer = Trace(countfuncs=1)
        tracer.run('{}()'.format(self.driver_function.__name__))
        results = tracer.results()
        called_functions = results.calledfuncs
        return called_functions
        # results.write_results()
