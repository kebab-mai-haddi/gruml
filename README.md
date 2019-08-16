# UML Generation

This repository deals with UML generation and plots the same in JSON, PDF and in Excel Spreadsheet.

## How to install?

The Python's requirements are listed in `requirements.txt` .
Install PyLint from [here](https://www.pylint.org/#install).
Also install GraphViz via `sudo apt install graphviz ` or the equivalent for your OS. Once Graphviz is installed make sure the bin folder is added to the PATH variable so that pyreverse can find it at run time.
For cross reference, take a look [here](https://gist.github.com/HarshaVardhanBabu/9a47db9e33cf06e9e1e917520bb54056).
My virtualenv is available [here](https://drive.google.com/drive/folders/1u0VfdaaorOzK_QKsRNfMuDfvRcQ76WGJ?usp=sharing)

## How to run?

Now that you are completed with the installation, run the following command:
`python3 generate_uml.py sample_class_module` where `sample_class_module` is the file that you want to generate the UML diagram for. Don't worry, the imported classes will also be plotted in the UML if they are inherited.

