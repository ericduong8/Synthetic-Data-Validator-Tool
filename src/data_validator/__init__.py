"""
Synthetic Data Validator - A tool for validating structured datasets in genomics and data-intensive pipelines.

This package provides validation for:
- Missing values in required fields
- Incorrect data types (e.g., strings where numbers are expected)
- Out-of-range values, such as negative expression levels or invalid dates
- Format consistency, ensuring each row conforms to a defined schema
"""

__version__ = "1.0.0"
__author__ = "Eric Duong"
__email__ = "duongmeric@gmail.com"

from .validators import validate_file
from .cli import cli

__all__ = ["validate_file", "cli"]
