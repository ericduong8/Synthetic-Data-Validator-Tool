import pandas as pd
import numpy as np

def report_missing(df: pd.DataFrame) -> list:
    missing = []
    for col in df.columns:
        null_count = df[col].isna().sum()
        if null_count:
            missing.append((col, int(null_count)))
    return missing

def report_outliers(df: pd.DataFrame) -> list:
    out = []
    for col in df.select_dtypes(include=[np.number]):
        series = df[col].dropna()
        q1, q3 = np.percentile(series, [25, 75])
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        mask = (series < lower) | (series > upper)
        if mask.any():
            out.append((col, int(mask.sum())))
    return out

def report_format_errors(data: dict) -> list:
    errors = []
    # e.g., require certain keys or types
    # if not isinstance(data.get("id"), int): errors.append("id must be integer")
    return errors
