import ast
import os
import pyclbr
import subprocess
import sys
from operator import itemgetter

from dependency_collector import ModuleUseCollector
from plot_uml_in_excel import WriteInExcel


class GenerateUML:
    def __init__(self):
        self.class_dict = {}  # it will have a class:children mapping.

    def show_class(self, name, class_data):
        print(class_data)
        self.class_dict[name] = []
        self.show_super_classes(name, class_data)

    def show_methods(self, class_name, class_data):
        methods = []
        for name, lineno in sorted(class_data.methods.items(),
                                   key=itemgetter(1)):
            # print('  Method: {0} [{1}]'.format(name, lineno))
            methods.append(name)
        return methods

    def show_super_classes(self, name, class_data):
        super_class_names = []
        for super_class in class_data.super:
            if super_class == 'object':
                continue
            if isinstance(super_class, str):
                super_class_names.append(super_class)
            else:
                super_class_names.append(super_class.name)
        for super_class_name in super_class_names:
            if self.class_dict.get(super_class_name, None):
                self.class_dict[super_class_name].append(name)
            else:
                self.class_dict[super_class_name] = [name]
        # adding all parents for a class in one place for later usage: children
        return super_class_names

    def get_children(self, name):
        if self.class_dict.get(name, None):
            return self.class_dict[name]
        return []


source_codes = ["transport", "car", "vehicles"]

# list of dicts where each dict is: {"name": <>, "methods": [], "children": []}
agg_data = []
# dictionary to store all files: classes mapping. If a .py file has three classes, their name, start and end line will be stored here.
files = {}
class_index = {}
counter = 0
# to check if a class has already been covered due to some import in another file.
classes_covered = {}

for source_code in source_codes:
    source_code_data = pyclbr.readmodule(source_code)
    generate_uml = GenerateUML()
    for name, class_data in sorted(source_code_data.items(), key=lambda x: x[1].lineno):
        print(
            "Class: {}, Methods: {}, Parent(s): {}, File: {}, Start line: {}, End line: {}".format(
                name,
                generate_uml.show_methods(
                    name, class_data
                ),
                generate_uml.show_super_classes(name, class_data),
                class_data.file,
                class_data.lineno,
                class_data.endline
            )
        )
        print('-----------------------------------------')
    print('=======================================')

    for name, class_data in sorted(source_code_data.items(), key=lambda x: x[1].lineno):
        methods = generate_uml.show_methods(name, class_data)
        children = generate_uml.get_children(name)
        if classes_covered.get(name):
            continue
        agg_data.append(
            {
                "Class": name,
                "Methods": methods,
                "Children": children,
                "File": class_data.file,
                "Start Line": class_data.lineno,
                "End Line": class_data.endline,
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
    if data['Dependents']:
        skip_cols += 1
    if data['Children']:
        skip_cols += 1
    print(data)
    print('========')
    print('\n')
    print('Skip cols are: {}'.format(skip_cols))

# The whole data is now collected and we need to form the dataframe of it:

write_in_excel = WriteInExcel(file_name='Dependency_2.xlsx')
df = write_in_excel.create_pandas_dataframe(agg_data, skip_cols)
write_in_excel.write_df_to_excel(
    df, 'sheet_one', skip_cols)

'''
print(generate_uml.class_dict)
write_in_excel = WriteInExcel(
    classes=generate_uml.class_dict, file_name='{}.xlsx'.format(source_code))
write_in_excel.form_uml_sheet_for_classes()
'''
