# README for the project

Please include information on:

## Background

* Why was the code written in the first place (nature of the project)?
* What the code does and how it does it.

For this template project:

* This template was developed to help the momdel*EAU* research team make their code more [FAIR](https://www.nature.com/articles/sdata201618) by implementing [Lee et al. (2021)'s barely sufficient coding practices](https://doi.org/10.1016/j.patter.2021.100206) which ask that scientific code be:
  
  *  Available
  *  Documented
  *  Version controlled
  *  Tested
  *  Supported

This repo was created to be used as a complete working example of those guidelines.

It implements a handful of python functions in the `.src/main.py` file. The file can be run using the command line (see below). 

Secret management is also implemented in this repo. The `secrets.yaml` file is meant to hold any confidential piece of information required to run your code. **Any new project using this repo must make sure that `secrets.yaml` is added to their `.gitignore` file!** Otherwise, you very well may share your secret usernames and passwords with the world!

The repo also provides sample tests for the sample code. The tests are meant to be run using the pytest package.

## Installation

* Outline the steps required to run the code on someone's machine.
In the case of this example:
* Navigate to the root directory of the project
* Create a virtual environment with the python version indicated in the file `.python-version` using either virtualenv or conda.
* Activate the virtual environment.
* run the command: `pip install -r requirements.txt` if you want to **use the project, but not contribute to it**.
* run the command: `pip install -r requirements-dev.txt`if you want to **contribute to the project**.

## Usage

Explain how to run the code. If the code is a library, how do you import it into your other projects? If the code is a script, what file should you run? with what command? What arguments?

In the case of this example:

* enter a value for "secret_token" in `secrets.yaml`
* enter the path to the csv file you want to process in `config.yaml` (source path)
* enter the name of the column you want to process in the `config.yaml` (column_to_process)
* enter the save path for the processed data in `config.yaml` (result_path)
* run the following commands

``` bash
# navigate to the src directory
cd src
# run the main file. See main.py for a description of the optional arguments.
python -m main
 ```

* Indicate what command(s) to run to test whether the code is running normally (if the code requires data to run, provide sampe data in the `./data` directory).

In the case of this example:

If the console prints out:

``` bash
FOO
FOO
FOO
FOO
FOO
secret token is <value of the 'secret_token' line of secrets.yaml>! Don't share it!
processing data...
done! saved to <result path from config.yaml>
```

Then everything worked as intended.

## Running tests

Having installed the project's required packages using the `requirements.txt` file, you can run the repo's automated tests by using the command `pytest` at the root directory of the project. 

Make sure the `pytest` package is installed in your developer environment by running `pip install -U pytest` at the root directory of the project. Then, run the `pytest` command. 

A report will be generated indicating whether any of the tests are failing.

## Contact information
Make sure that the contact info is up-to-date so that people can reach out if they have questions about the code or wish to bring up an issue.

### Current maintainer of the template:
Jean-David Therrien

email: jean-david.therrien.1@ulaval.ca

### To report a bug:

Please use GitHub's issues function, or send me an email.

### For questions:

Please reach out by email.

### Intended support period

This template was created as a support tool for a model*EAU* internal workshop. Though I intend to get it working and help my colleagues use it until the end of my PhD studies (2023), updates may not occur very often.

## References

If the code was produced in relation to a specific publication, add the reference and DOI of the publication.
