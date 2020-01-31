import sys

from trace import Trace
from driver import main_2
# tracer = trace.Trace( ignoredirs=[sys.prefix, sys.exec_prefix], trace=1, count=1)
tracer = Trace(countfuncs=1, countcallers=1, timing=1)
tracer.run('main_2()')
r = tracer.results()
for func in r.calledfuncs:
    print(func)
print('---------')
for func in r.callers:
    print(func)
