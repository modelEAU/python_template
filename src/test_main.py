"""This file contains functions used to test the functionality of functions in the project. Name each test with the prefix test_.
"""
import pandas as pd

import main


def test_square_series():
    # set up the data
    test_input = pd.Series([1, 2, 3, 4])

    expected_output = pd.Series([1, 4, 9, 16])

    assert main.square_series(test_input).equals(expected_output)
