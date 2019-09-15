import os
import pyclbr
import subprocess
import sys
from operator import itemgetter

from plot_uml_in_excel import WriteInExcel


class GenerateUML:
    def __init__(self):
        self.class_dict = {}

    def show_class(self, name, class_data):
        # print('Class:', name)
        self.class_dict[name] = []
        self.show_super_classes(name, class_data)
        # show_methods(name, class_data)
        # print()

    def show_methods(self, class_name, class_data):
        for name, lineno in sorted(class_data.methods.items(),
                                   key=itemgetter(1)):
            print('  Method: {0} [{1}]'.format(name, lineno))

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


# source_code = sys.argv[1]
source_code = "sample_class_module"
source_code_data = pyclbr.readmodule(source_code)
generate_uml = GenerateUML()
for name, class_data in sorted(source_code_data.items(),
                               key=lambda x: x[1].lineno):
    generate_uml.show_class(name, class_data)

print(generate_uml.class_dict)
write_in_excel = WriteInExcel(
    classes=generate_uml.class_dict, file_name='{}.xlsx'.format(source_code))
write_in_excel.form_uml_sheet_for_classes()

# plot the UML diagrams in PDF:
dot_file_subprocess_code = subprocess.run(
    ["pyreverse", "-S", "{}.py".format(source_code), "--all-ancestors", "-p", source_code]
)
if dot_file_subprocess_code.returncode != 0:
    raise ValueError(
        'Unable to create dot files!'
    )
pdf_generation_code = subprocess.run(
    ["dot", "-Tpdf", "classes_{}.dot".format(source_code), "-O"]
)
if pdf_generation_code.returncode != 0:
    raise ValueError(
        'Unable to create UML PDF file!'
    )
json_generation_code = subprocess.run(
    ["dot", "-Tjson", "classes_{}.dot".format(source_code), "-O"]
)
if json_generation_code.returncode != 0:
    raise ValueError(
        'Unable to create JSON file of the UML!'
    )
