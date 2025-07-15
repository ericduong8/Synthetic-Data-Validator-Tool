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
# Validate a single file
data-validator validate sample_data/valid_example.csv

# Validate multiple files
data-validator validate sample_data/valid_example.csv sample_data/invalid_example.csv
```

### Advanced Options
```bash
# Verbose output with detailed error breakdown
data-validator validate sample_data/invalid_example.csv --verbose

# Export detailed report to a JSON file
data-validator validate sample_data/invalid_example.csv --json-output report.json

```

### Example Output

**Valid dataset :**
```
$ data-validator validate sample_data/valid_example.csv
Validating 1 file(s)...
==================================================

File: sample_data/valid_example.csv
Status: PASS
Summary: 0 missing, 0 outlier(s), 0 type error(s)

==================================================
Validation Summary: 1/1 files passed
✓ All files passed validation!
```

**Invalid dataset with verbose output:**
```
$ data-validator validate sample_data/invalid_example.csv --verbose
Validating 1 file(s)...
==================================================

File: sample_data/invalid_example.csv
Status: FAIL
Summary: 4 missing, 6 outlier(s), 2 type error(s)
  Missing values:
    - age: 2 missing values
    - blood_sugar: 3 missing values
    - heart_rate: 2 missing values
    - hemoglobin: 3 missing values
  Outliers/Range violations:
    - age_domain_range: 5 outlier(s)
    - cholesterol_domain_range: 7 outlier(s)
    - blood_sugar_statistical: 2 outlier(s)
    - systolic_bp_statistical: 3 outlier(s)
    - diastolic_bp_statistical: 3 outlier(s)
    - temperature_domain_range: 2 outlier(s)
  Data type errors:
    - heart_rate: Mixed types: 97 numeric, 1 non-numeric
    - sample_date_date_format: 2 invalid date formats

==================================================
Validation Summary: 0/1 files passed
✗ 1 file(s) failed validation
```

## Sample Data

The repository includes comprehensive sample data files for testing:

- **`sample_data/valid_example.csv`**: 100 entries with 12 health attributes (age, cholesterol, blood_sugar, blood_pressure, heart_rate, BMI, temperature, hemoglobin, WBC count, sample_date). Contains 1 statistical outlier which is expected in larger datasets.
- **`sample_data/invalid_example.csv`**: 100 entries with 32+ intentional validation issues including missing values, out-of-range values, mixed data types, and invalid date formats.

## Genomics and Health Data Use Cases

This tool is specifically designed for quality control in:

- **Genomics Pipelines**: Validate gene expression data, sample metadata, and experimental results
- **Clinical Data**: Check patient records, lab results, and health measurements
- **Biobank Data**: Ensure specimen tracking and phenotype data integrity
- **Research Datasets**: Validate experimental data before analysis
- **Data Integration**: Check consistency when merging datasets from multiple sources

<!-- ## API Usage

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
``` -->

<!-- ## Testing

Run the comprehensive test suite:

```bash
# Install pytest
pip install pytest

# Run all tests
python -m pytest tests/ -v

# Run specific test categories
python -m pytest tests/test_validators.py::TestValidators::test_sample_data_files -v
``` -->

<!-- ## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new validation features
4. Ensure all tests pass
5. Submit a pull request

## License

This project is designed for genomics and data pipeline quality control applications. -->
