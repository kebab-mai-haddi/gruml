# GRUML
Tired of collaborating over UML diagrams or don't use them at all? We feel you. We know how tedious it is to use or even think of UML diagrams for large codebases.Thus, we bring you RUML - Rectangular UML diagrams. You can know what all classes are dependent on one another, who inherits from whom, what is the flow of control of your codebase when executed in different scenarios - all in an Excel sheet.

# Installation
## Changing pyclbr.py in cpython.
First, we need to update our pyclbr module as it is still [WIP](https://github.com/python/cpython/pull/16466#issuecomment-583693647) in CPython. Copy the source code from [here](https://pastebin.com/6WF65Lvk) and paste the contents in your pyclbr file:
### Mac users
`/usr/local/Cellar/python/3.7.7/Frameworks/Python.framework/Versions/3.7/lib/python3.7/pyclbr.py`
where `3.7` is the Python version you are using.
### Window users
TODO
### Linux users
TODO
## Cloning the source code
`git clone https://github.com/kebab-mai-haddi/generate_uml.git`

# Running the application
`cd generate_uml`

`python3 generate_ruml.py`

The command line will soon ask for your input which is the destination of the source code. This is where you enter the directory's address. For eg, I enter `/Users/aviralsrivastava/Desktop/source_codes_to_study/spiderfoot`
The command will then ask you to enter the use case or you can exit the program using `Ctrl-c`.

# Example
## A simple example
Download a source code from [here](https://drive.google.com/open?id=1EXCm04JnHUzMuytZ3iGul2IuLr0in6Of)

```
python3 generate_ruml.py
```
> Please enter the source code path
```
/Users/aviralsrivastava/Desktop/source_code_to_study/
```
> Please enter the use case or press Ctrl-c to exit the program:
```
random_name
```
> Please enter the driver path:
```
/Users/aviralsrivastava/Desktop/source_code_to_study/driver.py
```
> Please enter the driver name:
```
main_2
```
You will see, at the end: 
```
sheet_one done!
```
## A real example
If you run our code(master branch) on [Spiderfoot](https://github.com/smicallef/spiderfoot) source code, you will have an output something like [this](https://docs.google.com/spreadsheets/d/1lnKfrPYF90uyFJ_NoYWOFdR5sMolwc0H62FwLg0dLcw/edit?usp=sharing).