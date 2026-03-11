"""
Processing Utils
"""

import pandas as pd


def normalize_zip_code(values: pd.Series) -> pd.Series:
    return values.astype("string").str.extract(r"(\d{5})", expand=False)
