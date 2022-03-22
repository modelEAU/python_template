"""INSERT SUMMARY FOR THE FILE. The summary should explain:
* What the file contains.
* What the file does.
* How to run the file. Write the exact command, e.g:
    `python -m main --argument_1 value_1 --argument_2 --value_2`

    In the case of this example, use:
    python -m main -m <message> -i <iterations>

    Arguments:
        message (m): the message you want to print out to the console.
        iterations (i): The number of times you want to print it out.
"""
# Define imports at the top of the file
import argparse
from typing import Any, Dict

import pandas as pd
import yaml

# Define constants after the imports
DEFAULT_MESSAGE = "FOO"
DEFAULT_NUMBER_OF_ITERATIONS = 5
DEFAULT_CONFIG_PATH = "../config.yaml"
DEFAULT_SECRETS_PATH = "../secrets.yaml"


def say_hello(message: str, n_iterations: int) -> None:
    """Prints out its inputs n-number of times.

    Arguments:
        message -- The message to print out
        n_iterations -- How many times the mesage is printed.

    Returns:
        None
    """
    for _ in range(n_iterations):
        print(message)
    return None


def read_yaml(path: str) -> Dict[str, Any]:
    """Reads yaml files and returns their contents as a dictionary

    Arguments:
        path -- where the yaml file is

    Returns:
        the dictionary with the data of the file
    """
    with open(path) as f:
        return yaml.safe_load(f)


def read_data(data_path: str) -> pd.DataFrame:
    """Reads data from a csv file and returns it as a DataFrame.

    Arguments:
        data_path -- where the data is.

    Returns:
        a dataframe containing the data.
    """
    return pd.read_csv(data_path, index_col=0)


def square_series(series: pd.Series) -> pd.Series:
    """Takes a series of integers and returns the square of each element

    Arguments:
        series -- the series with the integers

    Returns:
        the squared series
    """
    return series ** 2


def save_data(df: pd.DataFrame, save_path: str) -> None:
    """Saves the processed data to a results file in csv format.

    Arguments:
        df -- the DataFrame with the processed data
        save_path -- where to save
    """
    return df.to_csv(save_path)


def play_with_data(load_path: str, save_path: str, column_name: str) -> None:
    """Example function that takes loads data, transforms it and then saves it.

    Arguments:
        load_path -- the path to the raw data
        save_path -- the path where we want to save the results
    """
    df = read_data(load_path)
    df[f'{column_name}_squared'] = square_series(df[column_name])
    print("processing data...")
    save_data(df, save_path)
    print(f"done! saved to {save_path}")


# A script should always have a main function where most of the logic is executed
# to avoid name conflicts in the global namespace.
def main(message: str, n_iterations: int, config_path: str, secrets_path: str) -> None:
    """_summary_

    Arguments:
        message -- _description_
        n_iterations -- _description_
        config_path -- _description_
        secrets_path -- _description_
    """
    say_hello(message, iterations)
    config = read_yaml(config_path)
    secrets = read_yaml(secrets_path)
    print(f"secret token is {secrets['secret_token']}! Don't share it!")
    play_with_data(config["source_path"], config["result_path"], config["column_to_process"])
    return None


# run the script only if it is called directly from the command line by placing it behind this "if" block
if __name__ == "__main__":
    # Define the arguments that can be passed in with the script
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--message', type=str, default=DEFAULT_MESSAGE, help='The message that you want to print.')
    parser.add_argument('-i', '--iterations', type=int, default=DEFAULT_NUMBER_OF_ITERATIONS, help='how many times you want to print it.')
    parser.add_argument('-c', '--config', type=str, default=DEFAULT_CONFIG_PATH, help='Where the configuration file is located')
    parser.add_argument('-s', '--secrets', type=str, default=DEFAULT_SECRETS_PATH, help='Where the configuration file is located')

    # parse the arguments that were passed in.
    args = parser.parse_args()
    message = args.message
    config_path = args.config
    secrets_path = args.secrets
    iterations = args.iterations

    # Run the main script with the arguments that were received
    main(message, iterations, config_path, secrets_path)
