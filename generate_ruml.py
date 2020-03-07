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

foo = None


class GRUML:

    def __init__(self, test=False):
        self.source_code_path = []
        self.source_code_modules = []
        self.driver_path = None
        self.driver_name = None
        self.test = test

    def get_source_code_path_and_modules(self):
        self.source_code_path = [input('Please enter the source code path \n')]
        for (dirpath, _, filenames) in os.walk(self.source_code_path[0]):
            for file in filenames:
                if file.endswith(".py"):
                    rel_dir = os.path.relpath(
                        dirpath, self.source_code_path[0])
                    file = os.path.join(rel_dir, file) if rel_dir != '.' else file
                    file = file.split(".py")[0]
                    self.source_code_modules += [file]
        print("Will be checking the following modules: ")
        print(self.source_code_modules)

    def get_driver_path_and_driver_name(self):
        use_case = input(
            'Please enter the use case or press Ctrl-c to exit the program: \n'
        )
        driver_path = input(
            'Please enter the driver path: \n'
        )
        driver_name = input(
            'Please enter the driver name: \n'
        )
        driver_function = input(
            'Please enter the driver function name: \n'
        )
        return use_case, driver_path, driver_name, driver_function

    def generate_dependency_data(self):
        agg_data = []
        # dictionary to store all files: classes mapping. If a .py file has three classes, their name, start and end line will be stored here.
        files = {}
        class_index = {}
        counter = 0
        # to check if a class has already been covered due to some import in another file.
        self.classes_covered = {}

        for source_code_module in self.source_code_modules:
            source_code_data = pyclbr.readmodule(
                source_code_module, path=self.source_code_path)
            generate_hierarchy = GenerateHierarchy()
            for name, class_data in sorted(source_code_data.items(), key=lambda x: x[1].lineno):
                if self.classes_covered.get(name):
                    continue
                methods = generate_hierarchy.show_methods(name, class_data)
                parents = generate_hierarchy.show_super_classes(
                    name, class_data)
                file_ = class_data.file
                start_line = class_data.lineno,
                end_line = class_data.end_lineno
                print("Class: {}, Methods: {}, Parent(s): {}, File: {}, Start line: {}, End line: {}".format(
                    name, methods, parents, file_, start_line, end_line))
                agg_data.append({"Class": name, "Methods": methods, "Parents": parents, "File": file_,
                                 "Start Line": start_line, "End Line": end_line, "Dependents": []})
                if files.get(class_data.file, None):
                    files[class_data.file].append(
                        {'class': name, 'start_line': class_data.lineno, 'end_line': class_data.end_lineno})
                else:
                    files[class_data.file] = [
                        {'class': name, 'start_line': class_data.lineno, 'end_line': class_data.end_lineno}]
                class_index[name] = counter
                counter += 1
                self.classes_covered[name] = 1
        print('\n')
        # extract inter-file dependencies i.e. if a file's classes have been used in other files. Files being modules here.
        for file_ in files.keys():
            module = file_.split('/')[-1].split('.py')[0]
            for j in files.keys():
                try:
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
                except AttributeError:
                    pass
        self.skip_cols = 0
        for data in agg_data:
            # if a class is dependent on this current class, a column has to be dedicated for this one.
            if data['Dependents'] or data['Parents']:
                self.skip_cols += 1
            print(data)
            print('========')
            print('\n')
            print('Skip cols are: {}'.format(self.skip_cols))
        # The whole data is now collected and we need to form the dataframe of it:
        self.write_in_excel = WriteInExcel(file_name='Dependency_2.xlsx')
        self.df = self.write_in_excel.create_pandas_dataframe(
            agg_data, self.skip_cols)
        self.write_in_excel.write_df_to_excel(
            self.df, 'sheet_one', self.skip_cols, self.classes_covered)

    def generate_sequential_function_calls(self):
        # generating sequence diagram for a use-case
        use_case, driver_path, driver_name, driver_function = self.get_driver_path_and_driver_name()
        generate_sequence_diagram = GenerateSequenceDiagram(
            driver_path, driver_name, self.source_code_path[0])
        spec = importlib.util.spec_from_file_location(driver_name, driver_path)
        global foo
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        tracer = Trace(countfuncs=1, countcallers=1, timing=1)
        tracer.run('foo.{}()'.format(driver_function))
        results = tracer.results()
        print('results of tracer are: ')
        print(results)
        caller_functions = results.callers
        function_sequence = []  # consists of all functions called in sequence
        for caller, callee in caller_functions:
            _, caller_module, caller_function = caller
            _, _, callee_function = callee
            if caller_module not in self.source_code_modules:
                continue
            function_sequence.append([caller_function, callee_function])
        print('Function sequence: ')
        for sequence in function_sequence:
            print(sequence)
        self.df = self.write_in_excel.integrate_sequence_diagram_in_df(
            self.df, function_sequence, use_case)
        print('Inside generate_ruml.py and the df formed after integrating sequence diagram is: ')
        print(self.df)
        print("Calling 2nd time, use case {}".format(use_case))
        self.write_in_excel.write_df_to_excel(
            self.df, 'sheet_one', self.skip_cols, self.classes_covered, use_case)


def main():
    gruml = GRUML()
    gruml.get_source_code_path_and_modules()
    gruml.generate_dependency_data()
    gruml.generate_sequential_function_calls()


main()
