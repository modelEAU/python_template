# README

## Background

As of 2022, there were several model*EAU* projects that had to re-implement a connection to the dateaubase. This repo attempts to consolidate all the required dateaubase functionality to promote code reuse.

The repo currently contains functions to:
- read dateaubase credentials and connection details from yaml files
- connect to a dateaubase instance
- perform queries to the dateaubase
- parse data files for data to upload into the dateaubase

## Installation

* Navigate to the root directory of the project
* Create a virtual environment with the python version indicated in the file `.python-version` using either virtualenv or conda.
* Activate the virtual environment.
* run the command: `pip install -r requirements.txt` if you want to **use the project, but not contribute to it**.
* run the command: `pip install -r requirements-dev.txt`if you want to **contribute to the project**.

## Usage

### Upload functionality

* enter dateaubase login credentials in `secrets.yaml`
* enter a description for the files you wish to parse (and the variables you wish to commit it to in the dateaubase) in the config_file_upload_test.yaml

* run the following commands

``` bash
# navigate to the src directory
cd src/dateaubase
# run the main file. See main.py for a description of the optional arguments.
python -m upload --local false --config "path/to/config/file/relative/to/upload/script"
 ```

Change the `local` flag to `true` if you are running the script from the dateaubase server (only do this if you are sure that your configuration is working!).

## Running tests

[There are currently no tests for this project]

Having installed the project's required packages using the `requirements.txt` file, you can run the repo's automated tests by using the command `pytest` at the root directory of the project.

Make sure the `pytest` package is installed in your developer environment by running `pip install -U pytest` at the root directory of the project. Then, run the `pytest` command.

A report will be generated indicating whether any of the tests are failing.

## Contact information

### Current maintainer:
Jean-David Therrien

email: jean-david.therrien.1@ulaval.ca

### To report a bug:

Please use GitHub's issues function, or send me an email.

### For questions:

Please reach out by email.

### Intended support period

This project should be maintained on an ongoing basis to allow model*EAU* students to carry on their research. I (Jean-David) will continue to support it personally until the end of my PD studies (circa 2023).

