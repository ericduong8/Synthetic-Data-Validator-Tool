# Synthetic Data Validator Tool

A comprehensive command-line tool for validating structured datasets used in genomics and data-intensive pipelines. The tool performs quality control checks on CSV and JSON files to ensure data integrity and compliance with expected formats.

## Features

The Synthetic Data Validator checks datasets for four critical validation types:

### 1. Missing Values Detection
- Identifies null, empty, or missing values in required fields
- Reports count and location of missing data points
- Essential for ensuring data completeness in genomics pipelines

### 2. Data Type Validation
- Detects mixed data types within columns (e.g., strings where numbers are expected)
- Validates date formats and scientific notation
- Identifies type coercion issues that could cause pipeline failures

### 3. Out-of-Range Value Detection
- **Statistical Outliers**: Uses IQR method to detect statistical anomalies
- **Domain-Specific Ranges**: Validates biological/health data constraints:
  - Age: 0-120 years
  - Cholesterol: 100-400 mg/dL
  - Expression levels: ≥0
  - Heart rate: 40-200 bpm
  - Temperature: 35-42°C
  - Blood pressure: 60-200 mmHg

### 4. Format Consistency Validation
- **CSV Files**: Ensures consistent data types and formats across rows
- **JSON Files**: Schema validation with required fields, type checking, and nested structure consistency
- Validates against configurable schemas for custom data formats

## Installation

```bash
# Install dependencies
pip install pandas numpy click

# Clone and install the tool
git clone https://github.com/ericduong8/Synthetic-Data-Validator-Tool.git
cd Synthetic-Data-Validator-Tool
pip install -e .
```

## Usage

### Basic Validation
```bash
# Validate single file
python -m src.data_validator.cli validate data.csv

# Validate multiple files
python -m src.data_validator.cli validate file1.csv file2.json file3.csv
```

### Advanced Options
```bash
# Verbose output with detailed error breakdown
python -m src.data_validator.cli validate data.csv --verbose

# Export detailed report to JSON
python -m src.data_validator.cli validate data.csv --json-output report.json

# Use custom schema for JSON validation
python -m src.data_validator.cli validate data.json --schema custom_schema.json
```

### Example Output
```
Validating 2 file(s)...
==================================================

File: sample_data/valid_example.csv
Status: PASS
Summary: 0 missing, 0 outlier(s), 0 type error(s)

File: sample_data/invalid_example.csv
Status: FAIL
Summary: 1 missing, 1 outlier(s), 1 type error(s)
  Missing values:
    - age: 1 missing values
  Outliers/Range violations:
    - age_domain_range: 1 outlier(s)
  Data type errors:
    - cholesterol: Mixed types: 1 numeric, 2 non-numeric

==================================================
Validation Summary: 1/2 files passed
✗ 1 file(s) failed validation
```

## Sample Data

The repository includes sample data files for testing:

- `sample_data/valid_example.csv`: Clean dataset that passes all validation checks
- `sample_data/invalid_example.csv`: Dataset with intentional issues for testing validation detection

## Genomics and Health Data Use Cases

This tool is specifically designed for quality control in:

- **Genomics Pipelines**: Validate gene expression data, sample metadata, and experimental results
- **Clinical Data**: Check patient records, lab results, and health measurements
- **Biobank Data**: Ensure specimen tracking and phenotype data integrity
- **Research Datasets**: Validate experimental data before analysis
- **Data Integration**: Check consistency when merging datasets from multiple sources

## API Usage

```python
from data_validator.validators import validate_file

# Validate a file programmatically
result = validate_file('data.csv')
print(f"Status: {result['status']}")
print(f"Issues found: {result['total_issues']}")

# Custom schema validation for JSON
schema = {
    'required_fields': ['sample_id', 'gene_name'],
    'field_types': {'sample_id': str, 'expression': float},
    'field_ranges': {'expression': (0, float('inf'))}
}
result = validate_file('data.json', schema=schema)
```

## Testing

Run the comprehensive test suite:

```bash
# Install pytest
pip install pytest

# Run all tests
python -m pytest tests/ -v

# Run specific test categories
python -m pytest tests/test_validators.py::TestValidators::test_sample_data_files -v
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new validation features
4. Ensure all tests pass
5. Submit a pull request

## License

This project is designed for genomics and data pipeline quality control applications.
