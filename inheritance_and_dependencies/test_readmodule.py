import os
import pyclbr
import sys

print(os.getcwd())
os.chdir('rto')
print(os.getcwd())
source_code = pyclbr.readmodule('car')
print(source_code)
source_code = pyclbr.readmodule('transport')
print(source_code)
source_code = pyclbr.readmodule('vehicles')
print(source_code)
