import pyclbr
import sys

source_code_module = 'contributors'
sys.path.insert(1, '/tmp/pandas/pandas/')
source_code_path = ['/tmp/pandas/pandas/doc/sphinxext']

print('sys.path is: ')
print(sys.path)

source_code_data = pyclbr.readmodule_ex(
    source_code_module, path=source_code_path)
print(source_code_data)