import pandas as pd
import json
from .utils import report_missing, report_outliers, report_format_errors

def validate_file(path: str) -> dict:
    if path.lower().endswith(".csv"):
        df = pd.read_csv(path)
        missing = report_missing(df)
        outliers = report_outliers(df)
        # you could have a schema for formats/ranges
        return {
            "missing": missing,
            "outliers": outliers,
            "summary": f"{len(missing)} missing, {len(outliers)} outlier(s)"
        }
    elif path.lower().endswith(".json"):
        data = json.load(open(path))
        fmt_errors = report_format_errors(data)
        # You might also convert to DataFrame if numeric
        return {
            "format_errors": fmt_errors,
            "summary": f"{len(fmt_errors)} format error(s)"
        }
    else:
        return {"summary": "Unsupported file type"}
