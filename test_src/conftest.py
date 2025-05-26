import pytest
import pandas as pd

@pytest.fixture()
def sample_data():
    return {
        "Age": 22,
        "WorkType":"Private",
        "Hypertension": 0,
        "HeartDisease": 0,
        "Married": "No",
        "Gender": "Female",
        "Residence": "Urban",
        "Bmi": 18.4,
        "GlucoseLevel": 89.6,
        "Smoking": "never smoked"
        }

@pytest.fixture()
def sample_wrong_data():
    return {
        "Age": "Young",
        "WorkType":"Private",
        "Hypertension": 0,
        "HeartDisease": 0,
        "Married": "No",
        "Gender": "Female",
        "Residence": "Urban",
        "Bmi": "Good",
        "GlucoseLevel": 89.6,
        "Smoking": "never smoked"
    }

@pytest.fixture()
def sample_wrong_format_data():
    return {
        "Name": "Tam",
        "Bod": 1101,
        "Sex": "Not defined"
    }