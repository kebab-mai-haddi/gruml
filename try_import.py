import sys
import importlib
from trace import Trace
sys.path.insert(
    1, '/Users/aviralsrivastava/Desktop/source_code_to_study/')

spec = importlib.util.spec_from_file_location(
    "driver", "/Users/aviralsrivastava/Desktop/source_code_to_study/driver.py")
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)
# foo.main_2()

tracer = Trace(countfuncs=1, )
tracer.run('foo.main_2()')
results = tracer.results()
print(results.calledfuncs)