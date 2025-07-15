import pytest
import pandas as pd
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_validator.validators import validate_file
from data_validator.utils import report_missing, report_outliers, report_type_errors, report_format_errors

class TestValidators:
    
    def test_report_missing(self):
        """Test missing value detection"""
        df = pd.DataFrame({"a": [1, None, 3], "b": [None, None, 2]})
        missing = dict(report_missing(df))
        assert missing["a"] == 1
        assert missing["b"] == 2

    def test_report_outliers_statistical(self):
        """Test statistical outlier detection"""
        df = pd.DataFrame({"x": [1, 2, 3, 100]})
        outliers = dict(report_outliers(df))
        assert outliers["x_statistical"] == 1

    def test_report_outliers_domain_range(self):
        """Test domain-specific range validation"""
        df = pd.DataFrame({"age": [25, 30, 150], "cholesterol": [180, 220, 500]})
        outliers = dict(report_outliers(df))
        assert outliers["age_domain_range"] == 1  # age 150 is out of range
        assert outliers["cholesterol_domain_range"] == 1  # cholesterol 500 is out of range

    def test_report_type_errors(self):
        """Test data type validation"""
        df = pd.DataFrame({
            "mixed_col": [1, 2, "not_a_number", 4],
            "numeric_col": [1, 2, 3, 4]
        })
        type_errors = dict(report_type_errors(df))
        assert "mixed_col" in type_errors
        assert "Mixed types" in type_errors["mixed_col"]
        assert "numeric_col" not in type_errors

    def test_report_format_errors_json(self):
        """Test JSON format validation"""
        data = {"age": 25}  # missing required 'id' field
        errors = report_format_errors(data)
        assert any("Missing required field: id" in error for error in errors)
        
        data = {"id": 1, "gene_name": 123}  # gene_name should be string
        errors = report_format_errors(data)
        assert any("incorrect type" in error for error in errors)
        
        data = {"id": 1, "age": 150}  # age out of range
        errors = report_format_errors(data)
        assert any("outside valid range" in error for error in errors)

    def test_validate_csv_file_valid(self):
        """Test CSV validation with valid data"""
        df = pd.DataFrame({
            "id": [1, 2, 3],
            "age": [25, 30, 35],
            "cholesterol": [180, 200, 220]
        })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            df.to_csv(f.name, index=False)
            result = validate_file(f.name)
            
        os.unlink(f.name)
        
        assert result["status"] == "PASS"
        assert result["total_issues"] == 0
        assert len(result["missing"]) == 0
        assert len(result["outliers"]) == 0
        assert len(result["type_errors"]) == 0

    def test_validate_csv_file_invalid(self):
        """Test CSV validation with invalid data"""
        df = pd.DataFrame({
            "id": [1, 2, 3],
            "age": [25, None, 150],  # missing value and out of range
            "cholesterol": [180, "invalid_text", 220]  # actual mixed types
        })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            df.to_csv(f.name, index=False)
            result = validate_file(f.name)
            
        os.unlink(f.name)
        
        assert result["status"] == "FAIL"
        assert result["total_issues"] > 0
        assert len(result["missing"]) > 0  # Should detect missing age
        assert len(result["outliers"]) > 0  # Should detect age=150 out of range
        assert len(result["type_errors"]) > 0  # Should detect mixed types in cholesterol

    def test_validate_json_file_valid(self):
        """Test JSON validation with valid data"""
        data = {
            "id": 1,
            "age": 25,
            "gene_name": "BRCA1",
            "expression_level": 5.2
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            f.close()  # Close file before reading
            result = validate_file(f.name)
            
        os.unlink(f.name)
        
        assert result["status"] == "PASS"
        assert result["total_issues"] == 0

    def test_validate_json_file_invalid(self):
        """Test JSON validation with invalid data"""
        data = {
            "age": 150,  # out of range, missing required 'id'
            "gene_name": 123,  # wrong type
            "expression_level": -5  # negative expression
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            f.close()  # Close file before reading
            result = validate_file(f.name)
            
        os.unlink(f.name)
        
        assert result["status"] == "FAIL"
        assert result["total_issues"] > 0
        assert len(result["format_errors"]) > 0

    def test_validate_unsupported_file(self):
        """Test validation with unsupported file type"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("some text")
            result = validate_file(f.name)
            
        os.unlink(f.name)
        
        assert result["status"] == "ERROR"
        assert "Unsupported file type" in result["summary"]

    def test_sample_data_files(self):
        """Test validation with the actual sample data files"""
        result = validate_file("sample_data/valid_example.csv")
        assert result["total_issues"] <= 2  # Allow for 1-2 statistical outliers in 100 entries
        assert len(result["missing"]) == 0  # Should have no missing values
        assert len(result["type_errors"]) == 0  # Should have no type errors
        
        result = validate_file("sample_data/invalid_example.csv")
        assert result["status"] == "FAIL"
        assert result["total_issues"] >= 10  # Should have many validation issues
        
        missing_cols = [col for col, count in result["missing"]]
        assert len(missing_cols) > 0  # Should detect missing values
        
        outlier_cols = [col for col, count in result["outliers"]]
        assert len(outlier_cols) > 0  # Should detect outliers/range violations
        
        type_error_cols = [col for col, error in result["type_errors"]]
        assert len(type_error_cols) > 0  # Should detect type errors
