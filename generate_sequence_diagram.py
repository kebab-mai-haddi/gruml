import importlib
import logging
import os
import sys
from trace import Trace

logging.basicConfig(level=logging.DEBUG)


class GenerateSequenceDiagram:
    def __init__(self, source_code_to_study_dir, driver_path=None, driver_module=None):
        '''
        source_code_to_study_dir
        '''
        # self.driver_module = __import__(driver_module)
        self.driver_path = driver_path
        self.driver_module = driver_module
        sys.path.insert(1, source_code_to_study_dir)
        sys.path.insert(2, os.getcwd())
        print(sys.path)
