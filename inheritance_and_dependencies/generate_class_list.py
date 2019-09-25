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


source_code = "car"
source_code_data = pyclbr.readmodule(source_code)
generate_uml = GenerateUML()
for name, class_data in sorted(source_code_data.items(), key=lambda x: x[1].lineno):
    print(
        "Class: {}, Methods: {}, Parent(s): {}, File: {}".format(
            name,
            generate_uml.show_methods(
                name, class_data
            ),
            generate_uml.show_super_classes(name, class_data),
            class_data.file
        )
    )
print('-----------------------------------------')
# create a list with all the data
# the frame of the list is: [{}, {}, {},....] where each dict is: {"name": <>, "methods": [], "children": []}
agg_data = []
files = {}
for name, class_data in sorted(source_code_data.items(), key=lambda x: x[1].lineno):
    methods = generate_uml.show_methods(name, class_data)
    children = generate_uml.get_children(name)
    print(
        "Class: {}, Methods: {}, Child(ren): {}, File: {}".format(
            name,
            methods,
            children,
            class_data.file
        )
    )
    agg_data.append(
        {
            "Class": name,
            "Methods": methods,
            "Children": children,
            "File": class_data.file
        }
    )
    files[class_data.file] = name
print('-----------------------------------------')
print(agg_data)


for data_index in range(len(agg_data)):
    module = agg_data[data_index]["File"].split('/')[-1].split('.py')[0]
    used_in = []
    for file_ in files.keys():
        if file_ == agg_data[data_index]["File"]:
            continue
        collector = ModuleUseCollector(module)
        source = open(file_).read()
        collector.visit(ast.parse(source))
        print('Module: {} used in file: {} at: {}'.format(
            module, file_, collector.used_at))
        if len(collector.used_at):
            used_in.append(files[file_])
    agg_data[data_index]['Dependents'] = used_in
'''
# checking the dependencies
dependencies = []
for data_index in range(len(agg_data)):
    collector = ModuleUseCollector(
        agg_data[data_index]['File'].split('/')[-1].split('.py')[0]
    )
    collector.visit(ast.parse(source))
    dependencies.append(collector.used_at)

agg_data[source_code_index]['Dependencies'] = dependencies
# next thing, for each class, find the dependency in each class.

'''
print('------------------------------------------------------------------')
print('FINAL')
for data in agg_data:
    print(data)
    print('-----------')
    print('\n')

# The whole data is now collected and we need to form the dataframe of it:

write_in_excel = WriteInExcel(file_name='dependency_1.xlsx')
df = write_in_excel.create_pandas_dataframe(agg_data)
sys.exit()
write_in_excel.write_df_to_excel(df, 'class_to_child')
'''
print(generate_uml.class_dict)
write_in_excel = WriteInExcel(
    classes=generate_uml.class_dict, file_name='{}.xlsx'.format(source_code))
write_in_excel.form_uml_sheet_for_classes()
'''