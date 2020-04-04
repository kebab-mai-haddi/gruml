import ast
import importlib
import logging
import os
import pyclbr
import sys
from collections import defaultdict
from trace import Trace

import pandas as pd

from dependency_collector import ModuleUseCollector
from generate_hierarchy import GenerateHierarchy
from generate_sequence_diagram import GenerateSequenceDiagram
from plot_uml_in_excel import WriteInExcel

foo = None

logging.basicConfig(level=logging.DEBUG)


class GRUML:

    def __init__(self, test=False):
        self.source_code_path = []
        self.source_code_modules = []
        self.driver_path = None
        self.driver_name = None
        self.test = test
        self.use_case = True

    def get_source_code_path_and_modules(self):
        """input source code that is to be studied and compute all
        modules inside it.
        """
        self.source_code_path = [input('Please enter the source code path \n')]
        for (dirpath, _, filenames) in os.walk(self.source_code_path[0]):
            for file in filenames:
                if file.endswith(".py"):
                    rel_dir = os.path.relpath(
                        dirpath, self.source_code_path[0])
                    file = os.path.join(
                        rel_dir, file) if rel_dir != '.' else file
                    file = file.split(".py")[0]
                    self.source_code_modules += [file]

    def get_driver_path_and_driver_name(self):
        """ask for driver path and driver module's  name.

        Returns:
            str, str, str, str -- returns use case, driver path, driver name, driver function.
        """
        use_case = input(
            'Please enter the use case or enter "N" if you want to skip use-case diagram generation: \n'
        )
        if use_case == 'N':
            self.use_case = False
            return
        self.use_case = use_case
        self.driver_path = input(
            'Please enter the driver path: \n'
        )
        self.driver_name = input(
            'Please enter the driver name: \n'
        )
        self.driver_function = input(
            'Please enter the driver function name: \n'
        )

    def generate_dependency_data(self):
        """generate dependency (inheritance and non-inheritance) data.
        """
        agg_data = []
        # dictionary to store all files: classes mapping. If a .py file has three classes, their name, start and end line will be stored here.
        files = {}
        class_index = {}
        counter = 0
        # to check if a class has already been covered due to some import in another file.
        self.classes_covered = {}

        for source_code_module in self.source_code_modules:
            source_code_module, source_code_path = os.path.basename(source_code_module), [os.path.join(
                self.source_code_path[0], os.path.dirname(source_code_module))]
            source_code_data = pyclbr.readmodule(
                source_code_module, path=source_code_path)
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
        logging.debug(' ---------------------------------- ')
        for _ in range(20):
            logging.debug('\n')
        for class_extra_index in range(len(agg_data)):
            class_extra = agg_data[class_extra_index]
            actual_parents = []
            if class_extra['Parents']:
                for parent in class_extra['Parents']:
                    parent_in_codebase = False
                    for classes in agg_data:
                        if classes['Class'] == parent:
                            parent_in_codebase = True
                            break
                    if not parent_in_codebase:
                        logging.debug('Class: {} has Parent: {} which is not in the entire codebase.'.format(
                            class_extra['Class'], parent))
                    else:
                        actual_parents.append(parent)
            agg_data[class_extra_index]['Parents'] = actual_parents
        logging.debug(' ---------------------------------- ')
        for _ in range(20):
            logging.debug('\n')
        for classes_extra in agg_data:
            logging.debug('Class: {}, Parent(s): {}'.format(
                classes_extra['Class'], classes_extra['Parents']))
        logging.debug(' ---------------------------------- ')
        for _ in range(20):
            logging.debug('\n')
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
                            logging.debug('Checking for class {} in file {} and _class is {}'.format(
                                class_, files[j], _class))
                            if ((class_['start_line'] < line_no) and (class_['end_line'] > line_no)):
                                agg_data[class_index[_class]]['Dependents'].append(class_[
                                    'class'])
                except AttributeError:
                    pass
                except KeyError as key_error:
                    logging.debug(
                        'Class {} was not found in agg_data but was brought up while checking non-inheritance dependencies, generating error: {}'.format(
                            _class, key_error
                        )
                    )
        self.skip_cols = 0
        parents_set = set()
        dependees_set = set()
        for data in agg_data:
            if data['Dependents']:
                dependees_set.add(data['Class'])
            if data['Parents']:
                for parent in data['Parents']:
                    parents_set.add(parent)
        self.skip_cols = len(parents_set) + len(dependees_set)
        # The whole data is now collected and we need to form the dataframe of it:
        self.write_in_excel = WriteInExcel(file_name='Dependency_2.xlsx')
        self.df = self.write_in_excel.create_pandas_dataframe(
            agg_data, self.skip_cols)
        self.write_in_excel.write_df_to_excel(
            self.df, 'sheet_one', self.skip_cols, self.classes_covered)

    def generate_sequential_function_calls(self):
        """generate sequential function calls
        for tracing source code and plotting sequence diagram.
        """
        # generating sequence diagram for a use-case
        generate_sequence_diagram = GenerateSequenceDiagram(
            self.driver_path, self.driver_name, self.source_code_path[0])
        spec = importlib.util.spec_from_file_location(
            self.driver_name, self.driver_path)
        global foo
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        tracer = Trace(countfuncs=1, countcallers=1, timing=1)
        tracer.run('foo.{}()'.format(self.driver_function))
        results = tracer.results()
        caller_functions = results.callers
        function_sequence = []  # consists of all functions called in sequence
        for caller, callee in caller_functions:
            _, caller_module, caller_function = caller
            _, _, callee_function = callee
            if caller_module not in self.source_code_modules:
                continue
            function_sequence.append([caller_function, callee_function])
        for sequence in function_sequence:
            logging.debug(sequence)
        self.df = self.write_in_excel.integrate_sequence_diagram_in_df(
            self.df, function_sequence, self.use_case)
        self.write_in_excel.write_df_to_excel(
            self.df, 'sheet_one', self.skip_cols, self.classes_covered, self.use_case)


def main():
    """driver function of GRUML.
    """
    gruml = GRUML()
    gruml.get_source_code_path_and_modules()
    gruml.get_driver_path_and_driver_name()
    gruml.generate_dependency_data()
    if gruml.use_case is True:
        gruml.generate_sequential_function_calls()


main()
