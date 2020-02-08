from trace import Trace
import importlib
import sys


class GenerateSequenceDiagram:
    def __init__(self, driver_path, driver_module, source_code_to_study_dir):
        # self.driver_module = __import__(driver_module)
        self.driver_path = driver_path
        self.driver_module = driver_module
        sys.path.insert(1, source_code_to_study_dir)

    def get_called_functions(self, driver_function):
        """return the called functions in their called sequence

        Returns:
            list(dict) -- called functions returned in a list(sorted) comprising of a dict keyed on filename, modulename and funcname.
        """
        # spec = importlib.util.spec_from_file_location(
        #     self.driver_module, self.driver_path)
        # foo = importlib.util.module_from_spec(spec)
        # spec.loader.exec_module(foo)
        # # main_2 = foo.main_2()
        # tracer = Trace(countfuncs=1)
        # function_to_be_called = foo.__getattribute__('main_2')
        # print(dir(function_to_be_called))
        # func_name = function_to_be_called.__name__
        # tracer.run('{}()'.format(func_name)) #resolve hardcoded driver function.
        # results = tracer.results()
        # print(results.calledfuncs)
        spec = importlib.util.spec_from_file_location(
            "driver", "/Users/aviralsrivastava/Desktop/source_code_to_study/driver.py")
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        # foo.main_2()
        tracer = Trace(countfuncs=1, )
        tracer.run('foo.main_2()')
        results = tracer.results()
        return results.calledfuncs
