# tests/test_validators.py
import pandas as pd
from data_validator.utils import report_missing, report_outliers

def test_report_missing():
    df = pd.DataFrame({"a":[1, None, 3], "b":[None,None,2]})
    miss = dict(report_missing(df))
    assert miss["a"] == 1
    assert miss["b"] == 2

def test_report_outliers():
    df = pd.DataFrame({"x":[1,2,3,100]})
    out = dict(report_outliers(df))
    # 100 is an outlier
    assert out["x"] == 1
