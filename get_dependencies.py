import os
import pyclbr
import subprocess
import sys
from operator import itemgetter

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
        class_data_methods = class_data.methods.items()
        for name, lineno in sorted(class_data_methods,
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
# source_code = "sample_class_module"
source_code = "aviral_gauri"
source_code_data = pyclbr.readmodule(source_code)
generate_uml = GenerateUML()
for name, class_data in sorted(source_code_data.items(), key=lambda x: x[1].lineno):
    print(
        "Class: {}, Methods: {}, Parent(s): {}".format(
            name,
            generate_uml.show_methods(
                name, class_data
            ),
            generate_uml.show_super_classes(name, class_data)
        )
    )
print('-----------------------------------------')
# create a list with all the data
# the frame of the list is: [{}, {}, {},....] where each dict is: {"name": <>, "methods": [], "children": []}
agg_data = []
for name, class_data in sorted(source_code_data.items(), key=lambda x: x[1].lineno):
    methods = generate_uml.show_methods(name, class_data)
    children = generate_uml.get_children(name)
    print(
        "Class: {}, Methods: {}, Child(ren): {}".format(
            name,
            methods,
            children
        )
    )
    agg_data.append(
        {
            "Class": name,
            "Methods": methods,
            "Children": children
        }
    )
print('-----------------------------------------')
print(agg_data)
write_in_excel = WriteInExcel(file_name='testing_1.xlsx')
df = write_in_excel.create_pandas_dataframe(agg_data)
write_in_excel.write_df_to_excel(df, 'class_to_child')

# print(generate_uml.class_dict)
# write_in_excel = WriteInExcel(
#     classes=generate_uml.class_dict, file_name='{}.xlsx'.format(source_code))
# write_in_excel.form_uml_sheet_for_classes()
