import pandas as pd
import json
from .utils import report_missing, report_outliers, report_format_errors, report_type_errors
from typing import Optional

def validate_file(path: str, schema: Optional[dict] = None) -> dict:
    """
    Validate a data file for missing values, data type errors, outliers, and format consistency.
    
    Args:
        path: Path to the file to validate
        schema: Optional schema for JSON validation or custom validation rules
        
    Returns:
        Dictionary containing validation results and summary
    """
    if path.lower().endswith(".csv"):
        try:
            df = pd.read_csv(path)
            missing = report_missing(df)
            outliers = report_outliers(df)
            type_errors = report_type_errors(df)
            
            total_issues = len(missing) + len(outliers) + len(type_errors)
            
            return {
                "missing": missing,
                "outliers": outliers,
                "type_errors": type_errors,
                "total_issues": total_issues,
                "summary": f"{len(missing)} missing, {len(outliers)} outlier(s), {len(type_errors)} type error(s)",
                "status": "PASS" if total_issues == 0 else "FAIL",
                "file_type": "CSV"
            }
        except Exception as e:
            return {
                "error": f"Failed to read CSV file: {str(e)}",
                "summary": "File read error",
                "status": "ERROR",
                "file_type": "CSV"
            }
            
    elif path.lower().endswith(".json"):
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            
            fmt_errors = report_format_errors(data, schema)
            
            return {
                "format_errors": fmt_errors,
                "total_issues": len(fmt_errors),
                "summary": f"{len(fmt_errors)} format error(s)",
                "status": "PASS" if len(fmt_errors) == 0 else "FAIL",
                "file_type": "JSON"
            }
        except json.JSONDecodeError as e:
            return {
                "error": f"Invalid JSON format: {str(e)}",
                "summary": "JSON parse error",
                "status": "ERROR",
                "file_type": "JSON"
            }
        except Exception as e:
            return {
                "error": f"Failed to read JSON file: {str(e)}",
                "summary": "File read error", 
                "status": "ERROR",
                "file_type": "JSON"
            }
    else:
        return {
            "error": "Unsupported file type",
            "summary": "Unsupported file type - only CSV and JSON are supported",
            "status": "ERROR",
            "file_type": "UNKNOWN"
        }
