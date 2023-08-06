This project will be used for automation scripts for setting up a new project. The goal is to have a single command that will set up a new project with the following:

Here is a possible structure we are thinking about.
project-automation/
├── setup.py
├── requirements.txt
├── config/
│ ├── aws_credentials.json
│ └── django_credentials.json
├── scripts/
│ ├── react_native_setup.py
│ ├── aws_setup.py
│ └── django_setup.py
├── utils/
│ ├── aws_util.py
│ ├── django_util.py
│ └── react_native_util.py
└── main.py

setup.py: The setup file for packaging your project.
requirements.txt: A file containing the dependencies required for your project.
config/: A directory to store the configuration files for AWS and Django credentials.
scripts/: A directory to store the scripts for setting up credentials for each component.
utils/: A directory to store utility functions or modules for interacting with AWS, Django, and React Native.
main.py: The entry point of your automation tool where you can orchestrate the setup process.
