"""Module for computing target column characteristics."""

from typing import Tuple


def get_jupyter_nb_code_to_get_target(target_column: str) -> Tuple[str, str]:
    """Return the code to get the target column from the dataframe.

    param target_column: The name of the target column.
    type target_column: str
    return: The markdown and code to get the target column from the dataframe
    rtype: Tuple[str, str]
    """
    markdown = "### Set the target column name"
    code = "target_column = '{}'".format(target_column)
    return markdown, code
