import pandas as pd
import numpy as np
import re
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional

def report_missing(df: pd.DataFrame) -> list:
    missing = []
    for col in df.columns:
        null_count = df[col].isna().sum()
        if null_count:
            missing.append((col, int(null_count)))
    return missing

def report_outliers(df: pd.DataFrame, domain_ranges: Optional[Dict[str, Tuple[float, float]]] = None, iqr_multiplier: float = 2.5) -> list:
    out = []
    
    default_ranges = {
        'age': (0, 120),
        'cholesterol': (100, 400),
        'expression': (0, float('inf')),
        'temperature': (35, 42),
        'heart_rate': (40, 200),
        'blood_pressure': (60, 200)
    }
    
    ranges = domain_ranges or default_ranges
    
    for col in df.select_dtypes(include=[np.number]):
        series = df[col].dropna()
        
        domain_violations = 0
        col_lower = str(col).lower()
        for domain_key, (min_val, max_val) in ranges.items():
            if domain_key in col_lower:
                domain_mask = (series < min_val) | (series > max_val)
                domain_violations = int(domain_mask.sum())
                if domain_violations > 0:
                    out.append((f"{col}_domain_range", domain_violations))
                break
        
        if len(series) >= 4:  # Need at least 4 values for meaningful IQR
            q1, q3 = np.percentile(series, [25, 75])
            iqr = q3 - q1
            if iqr > 0:  # Avoid division by zero
                lower, upper = q1 - iqr_multiplier * iqr, q3 + iqr_multiplier * iqr
                mask = (series < lower) | (series > upper)
                statistical_outliers = int(mask.sum())
                if statistical_outliers > 0 and domain_violations == 0:  # Don't double-count
                    out.append((f"{col}_statistical", statistical_outliers))
    
    return out

def report_type_errors(df: pd.DataFrame) -> list:
    errors = []
    
    for col in df.columns:
        series = df[col].dropna()
        if len(series) == 0:
            continue
            
        numeric_count = 0
        string_count = 0
        
        for value in series:
            if isinstance(value, (int, float, np.number)):
                numeric_count += 1
            elif isinstance(value, str):
                try:
                    float(value)
                    numeric_count += 1
                except ValueError:
                    if re.match(r'^-?\d*\.?\d+[eE][+-]?\d+$', str(value)):
                        numeric_count += 1
                    else:
                        string_count += 1
            else:
                string_count += 1
        
        if numeric_count > 0 and string_count > 0:
            errors.append((col, f"Mixed types: {numeric_count} numeric, {string_count} non-numeric"))
        
        if 'date' in str(col).lower() or 'time' in str(col).lower():
            invalid_dates = 0
            for value in series:
                if isinstance(value, str):
                    try:
                        datetime.fromisoformat(value.replace('Z', '+00:00'))
                    except ValueError:
                        try:
                            datetime.strptime(value, '%Y-%m-%d')
                        except ValueError:
                            try:
                                datetime.strptime(value, '%m/%d/%Y')
                            except ValueError:
                                invalid_dates += 1
            
            if invalid_dates > 0:
                errors.append((f"{col}_date_format", f"{invalid_dates} invalid date formats"))
    
    return errors

def report_format_errors(data: dict, schema: Optional[Dict[str, Any]] = None) -> list:
    errors = []
    
    default_schema = {
        'required_fields': ['id'],
        'field_types': {
            'id': (int, str),
            'age': (int, float),
            'expression_level': (int, float),
            'gene_name': str,
            'sample_id': (int, str)
        },
        'field_ranges': {
            'age': (0, 120),
            'expression_level': (0, float('inf'))
        }
    }
    
    schema = schema or default_schema
    
    if 'required_fields' in schema:
        for field in schema['required_fields']:
            if field not in data:
                errors.append(f"Missing required field: {field}")
    
    if 'field_types' in schema:
        for field, expected_types in schema['field_types'].items():
            if field in data:
                value = data[field]
                if not isinstance(expected_types, tuple):
                    expected_types = (expected_types,)
                
                if not isinstance(value, expected_types):
                    errors.append(f"Field '{field}' has incorrect type: expected {expected_types}, got {type(value)}")
    
    if 'field_ranges' in schema:
        for field, (min_val, max_val) in schema['field_ranges'].items():
            if field in data:
                value = data[field]
                if isinstance(value, (int, float)):
                    if value < min_val or value > max_val:
                        errors.append(f"Field '{field}' value {value} outside valid range [{min_val}, {max_val}]")
    
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                if len(value) > 1:
                    first_item_type = type(value[0])
                    if isinstance(value[0], dict):
                        first_keys = set(value[0].keys())
                        for i, item in enumerate(value[1:], 1):
                            if not isinstance(item, dict):
                                errors.append(f"Inconsistent list item type in '{key}' at index {i}")
                            elif set(item.keys()) != first_keys:
                                errors.append(f"Inconsistent object structure in '{key}' at index {i}")
                    else:
                        for i, item in enumerate(value[1:], 1):
                            if type(item) != first_item_type:
                                errors.append(f"Inconsistent list item type in '{key}' at index {i}")
    
    return errors
