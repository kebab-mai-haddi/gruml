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
        # print(class_data)
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


# source_code = sys.argv[1]
source_code = "car"
source_code_data = pyclbr.readmodule(source_code)
generate_uml = GenerateUML()
# print('-----------------------------------------')
# create a list with all the data
# the frame of the list is: [{}, {}, {},....] where each dict is: {"name": <>, "methods": [], "children": []}
agg_data = []
for name, class_data in sorted(source_code_data.items(), key=lambda x: x[1].lineno):
    methods = generate_uml.show_methods(name, class_data)
    children = generate_uml.get_children(name)
    agg_data.append(
        {
            "Class": name,
            "Methods": methods,
            "Children": children,
            "File": class_data.file
        }
    )
# print('-----------------------------------------')
# print(agg_data)

# Get the dependencies by specifying all the files for each file.
for data in agg_data:
    print(data)
    print('\n')
import sys
sys.exit()
for data_index in range(len(agg_data)):
    collector = ModuleUseCollector(
        agg_data[data_index]['File'].split('/')[-1].split('.py')[0])
    source = open("{}.py".format(source_code)).read()
    collector.visit(ast.parse(source))
    # print(
    #     "Checking file: {} in source code: {}, these are the places where it is used: {}".format(
    #         agg_data[data_index]['File'], source_code, collector.used_at
    #     )
    # )
    agg_data[data_index]['Dependencies'] = collector.used_at

for data in agg_data:
    print(data)
    print('\n')


# write_in_excel = WriteInExcel(file_name='testing_1.xlsx')
# df = write_in_excel.create_pandas_dataframe(agg_data)
# write_in_excel.write_df_to_excel(df, 'class_to_child')
