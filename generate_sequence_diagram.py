from trace import Trace
import importlib
import sys

class GenerateSequenceDiagram:
    def __init__(self, driver_path, source_code_dir):
        # self.driver_module = __import__(driver_module)
        self.driver_path = driver_path
        self.source_code_dir = source_code_dir

    def get_called_functions(self):
        """return the called functions in their called sequence

        Returns:
            list(dict) -- called functions returned in a list(sorted) comprising of a dict keyed on filename, modulename and funcname.
        """
        import subprocess
        command = ["python3", "-m", "trace",
                   "-t", "{}".format(self.driver_path)]
        called_functions = subprocess.run(
            command,
            stdout=subprocess.PIPE
        ).stdout.decode('utf-8').split('\n')
        modules_to_be_traced = []
        for file_ in os.listdir(self.source_code_dir):
            if file_.endswith(".py"):
                modules_to_be_traced.append(file_.split('.py')[0])
        functions = []
        for called_function in called_functions:
            if '--- modulename' not in called_function:
                continue
            right_module = False
            for module in modules_to_be_traced:
                if module not in called_function:
                    continue
                right_module = True
                break
            if not right_module:
                continue
            called_function = called_function.split(',')
            functions.append(
                {
                    'modulename': called_function[0].split(': ')[1],
                    'funcname': called_function[1].split(': ')[1]
                }
            )
        return functions


ob = GenerateSequenceDiagram(
    '/Users/aviralsrivastava/Desktop/source_code_to_study/driver.py', '/Users/aviralsrivastava/Desktop/source_code_to_study/')
print(ob.get_called_functions())
'''
["python3", "-m", "trace", "--ignore-module '_bootstrap'", "--ignore-module '_bootstrap_external'",
    "--trace", "/Users/aviralsrivastava/Desktop/source_code_to_study/driver.py"]

[
    "python3", "-m", "trace", "--trace", "-C", ".", "/Users/aviralsrivastava/Desktop/source_code_to_study/driver.py"
]
a = [
    "python3",
    "-m",
    "trace",
    "-t",
    "--ignore-module='_bootstrap'",
    "--ignore-module='_bootstrap_external'",
    "/Users/aviralsrivastava/Desktop/source_code_to_study/driver.py"
]
.stdout.decode('utf-8')
'''