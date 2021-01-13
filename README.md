# GRUML
Tired of collaborating over UML diagrams or don't use them at all? We feel you. We know how tedious it is to use or even think of UML diagrams for large codebases.Thus, we bring you RUML - Rectangular UML diagrams. You can know what all classes are dependent on one another, who inherits from whom, what is the flow of control of your codebase when executed in different scenarios - all in an Excel sheet.

# Installation
## Docker
Click [here](https://docs.docker.com/get-docker/) to install Docker.
## Install GRUML
`docker run -d --name gruml avisrivastava254084/gruml:latest`
# Running the application
`docker exec gruml python3 generate_ruml.py --help`

# Example
## A simple example
```docker exec gruml python3 generate_ruml.py https://github.com/kebab-mai-haddi/python3-class-inheritance-dependency-example -u test_cli -d driver -dp driver.py -df main_2```

```docker cp gruml://home/ubuntu/generate_uml/Use_Case_test_cliDependency_2.xlsx demo_video.xlsx```

Open the `demo_video.xlsx` file and see the visualization of the codebase.