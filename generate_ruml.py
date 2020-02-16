import ast
import importlib
import os
import pyclbr
import sys
from trace import Trace

import pandas as pd

from dependency_collector import ModuleUseCollector
from generate_hierarchy import GenerateHierarchy
from generate_sequence_diagram import GenerateSequenceDiagram
from plot_uml_in_excel import WriteInExcel

source_code_path = []
source_code_modules = []
driver_path = None
driver_name = None


def get_source_code_path_and_modules():
    global source_code_path, source_code_modules, driver_path, driver_name
    source_code_path = [input('Please enter the source code path \n')]
    # fetch all the modules
    for file_ in os.listdir(source_code_path[0]):
        if file_.endswith(".py") and not file_.startswith('driver'):
            source_code_modules.append(file_.split('.py')[0])
    print(source_code_modules)


get_source_code_path_and_modules()


def get_driver_path_and_driver_name():
    use_case = input(
        'Please enter the use case or press Ctrl-c to exit the program: \n'
    )
    driver_path = input(
        'Please enter the driver path: \n'
    )
    driver_name = input(
        'Please enter the driver name: \n'
    )
    return use_case, driver_path, driver_name


# list of dicts where each dict is: {"name": <>, "methods": [], "children": []}
agg_data = []
# dictionary to store all files: classes mapping. If a .py file has three classes, their name, start and end line will be stored here.
files = {}
class_index = {}
counter = 0
# to check if a class has already been covered due to some import in another file.
classes_covered = {}

for source_code_module in source_code_modules:
    source_code_data = pyclbr.readmodule(
        source_code_module, path=source_code_path)
    generate_hierarchy = GenerateHierarchy()
    for name, class_data in sorted(source_code_data.items(), key=lambda x: x[1].lineno):
        if classes_covered.get(name):
            continue
        methods = generate_hierarchy.show_methods(name, class_data)
        parents = generate_hierarchy.show_super_classes(name, class_data)
        file_ = class_data.file
        start_line = class_data.lineno,
        end_line = class_data.end_lineno
        print(
            "Class: {}, Methods: {}, Parent(s): {}, File: {}, Start line: {}, End line: {}".format(
                name,
                methods,
                parents,
                file_,
                start_line,
                end_line
            )
        )
        agg_data.append(
            {
                "Class": name,
                "Methods": methods,
                "Parents": parents,
                "File": file_,
                "Start Line": start_line,
                "End Line": end_line,
                "Dependents": []
            }
        )
        if files.get(class_data.file, None):
            files[class_data.file].append(
                {
                    'class': name,
                    'start_line': class_data.lineno,
                    'end_line': class_data.end_lineno
                }
            )
        else:
            files[class_data.file] = [
                {
                    'class': name,
                    'start_line': class_data.lineno,
                    'end_line': class_data.end_lineno
                }
            ]
        class_index[name] = counter
        counter += 1
        classes_covered[name] = 1
print('\n')
# extract inter-file dependencies i.e. if a file's classes have been used in other files. Files being modules here.
for file_ in files.keys():
    module = file_.split('/')[-1].split('.py')[0]
    for j in files.keys():
        source = open(j).read()
        collector = ModuleUseCollector(module)
        collector.visit(ast.parse(source))
        for use_ in collector.used_at:
            _class = use_[0].split(".")[-1]
            alias = use_[1]
            line_no = use_[2]
            for class_ in files[j]:
                if ((class_['start_line'] < line_no) and (class_['end_line'] > line_no)):
                    agg_data[class_index[_class]]['Dependents'].append(class_[
                                                                       'class'])

# checking intra-file dependencies i.e. if a class is used in another class of the same module(file).


print('FINAL')
skip_cols = 0
for data in agg_data:
    # if a class is dependent on this current class, a column has to be dedicated for this one.
    if data['Dependents'] or data['Parents']:
        skip_cols += 1
    print(data)
    print('========')
    print('\n')
    print('Skip cols are: {}'.format(skip_cols))

# The whole data is now collected and we need to form the dataframe of it:

write_in_excel = WriteInExcel(file_name='Dependency_2.xlsx')
df = write_in_excel.create_pandas_dataframe(agg_data, skip_cols)
write_in_excel.write_df_to_excel(
    df, 'sheet_one', skip_cols, classes_covered)

# generating sequence diagram for a use-case
use_case, driver_path, driver_name = get_driver_path_and_driver_name()
generate_sequence_diagram = GenerateSequenceDiagram(
    driver_path,
    driver_name,
    source_code_path[0]
)
spec = importlib.util.spec_from_file_location(
    driver_name, driver_path)
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)
tracer = Trace(countfuncs=1, countcallers=1, timing=1)
tracer.run('foo.main_2()')
results = tracer.results()
print('results of tracer are: ')
print(results)
caller_functions = results.callers
function_sequence = []  # consists of all functions called in sequence
for caller, callee in caller_functions:
    caller_file, caller_module, caller_function = caller
    callee_file, callee_module, callee_function = callee
    if caller_module not in source_code_modules:
        continue
    function_sequence.append([caller_function, callee_function])

print('Function sequence: ')
for sequence in function_sequence:
    print(sequence)

df = write_in_excel.integrate_sequence_diagram_in_df(
    df, function_sequence, use_case)
print('Inside generate_ruml.py and the df formed after integrating sequence diagram is: ')
print(df)

print("Calling 2nd time, use case {}".format(use_case))
write_in_excel.write_df_to_excel(
    df, 'sheet_one', skip_cols, classes_covered, use_case)
