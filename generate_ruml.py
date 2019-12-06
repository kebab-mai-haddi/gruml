from source_code_to_study.trace_functions_called import GenerateSequenceDiagram
import ast
import pyclbr

from dependency_collector import ModuleUseCollector
from generate_hierarchy import GenerateHierarchy
from plot_uml_in_excel import WriteInExcel

source_codes = ["source_code_to_study/transport",
                "source_code_to_study/car", "source_code_to_study/vehicles"]

# list of dicts where each dict is: {"name": <>, "methods": [], "children": []}
agg_data = []
# dictionary to store all files: classes mapping. If a .py file has three classes, their name, start and end line will be stored here.
files = {}
class_index = {}
counter = 0
# to check if a class has already been covered due to some import in another file.
classes_covered = {}

for source_code in source_codes:
    source_code = source_code.split('/')
    source_code_data = pyclbr.readmodule(source_code[-1], source_code[0:-1])
    generate_hierarchy = GenerateHierarchy()
    for name, class_data in sorted(source_code_data.items(), key=lambda x: x[1].lineno):
        if classes_covered.get(name):
            continue
        methods = generate_hierarchy.show_methods(name, class_data)
        parents = generate_hierarchy.show_super_classes(name, class_data)
        file_ = class_data.file
        start_line = class_data.lineno,
        end_line = class_data.endline
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
                    'end_line': class_data.endline
                }
            )
        else:
            files[class_data.file] = [
                {
                    'class': name,
                    'start_line': class_data.lineno,
                    'end_line': class_data.endline
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
df = write_in_excel.create_pandas_dataframe(
    agg_data, skip_cols)
write_in_excel.write_df_to_excel(
    df, 'sheet_one', skip_cols)

# generate sequence diagram

generate_sequence_diagram = GenerateSequenceDiagram('driver')
called_functions = generate_sequence_diagram.get_called_functions('main_2')
for filename, modulename, funcname in called_functions:
    print('filename: {}, modulename: {}, funcname: {}'.format(
        filename, modulename, funcname))
