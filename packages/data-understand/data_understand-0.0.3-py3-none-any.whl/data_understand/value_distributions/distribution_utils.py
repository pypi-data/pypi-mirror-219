"""Module contains common utilities for computing distributions."""

from typing import List, Tuple

import pandas as pd


def get_categorical_features(df: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """Get the categorical features from a dataframe.

    :param df: The dataframe to get the categorical features from.
    :type df: pd.DataFrame
    :return: A tuple of lists of categorical and non-categorical features.
    :rtype: Tuple[List[str], List[str]]
    """
    numeric_features = set(df.select_dtypes(include="number").columns.tolist())
    all_features = set(df.columns.tolist())
    return numeric_features, list(all_features - numeric_features)
