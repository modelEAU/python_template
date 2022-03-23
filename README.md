# README for the project

Please include information on:

## Background

* Why was the code written in the first place (nature of the project)?
* What the code does and how it does it.

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
# run the main file. See msin.py for a description of the optional arguments.
python -m main
 ```

* Indicate what command(s) to run to test whether the code is running normally (if the code requires data to run, provide sampe data in the `./data` directory).

In the case of this example:

If the console prints out:

``` bash
"FOO
FOO
FOO
FOO
FOO
secret token is <secret token from secrets.yaml>! Don't share it!
processing data...
done! saved to <result path from config.yaml>"
```

Then everything worked as intended.

## Contact information
Make sure that the contact info is up-to-date so that people can reach out of they have questions about the code or wish to bring up an issue.

### Current maintainer:
Jean-David Therrien

email: jean-david.therrien.1@ulaval.ca

### To report a bug:

Please use GitHub's issues function, send me an email.

### For questions:

Please reach out by email.

### Intended support period

This template was created as a support tool for an internal workshop. Though I intend to get it working and help my colleagues use it until the end of my PhD studies (2023), updates may not occur very often.

## References

If the code was produced in relation to a specific publication, add the reference and DOI of the publication.
