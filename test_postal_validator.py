# test_postal_validator.py

import pytest
from postal_validator import validate_dutch_postal_code
import os
import sqlite3

# This test file now only needs to test the logic, not the data.
# The data is managed by the data layer and tested in test_app.py.

# Define the database file name
DATABASE_FILE = "postal_prefixes.db"


@pytest.fixture(autouse=True)
def setup_database_for_tests():
    # Setup a mock database for the tests to use.
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE postal_prefixes (id INTEGER PRIMARY KEY, prefix TEXT NOT NULL UNIQUE)"
    )
    initial_prefixes = [("10",), ("60",)]  # A small set for clean testing
    cursor.executemany(
        "INSERT INTO postal_prefixes (prefix) VALUES (?)", initial_prefixes
    )
    conn.commit()
    conn.close()

    yield

    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)


def test_standard_postal_code_valid():
    postal_code = "1012 AB"
    result = validate_dutch_postal_code(postal_code)
    assert result["status"] == "success"


def test_non_standard_postal_code_numeric_prefix():
    postal_code = "0123 AB"
    result = validate_dutch_postal_code(postal_code)
    assert result["status"] == "warning"


def test_invalid_short_postal_code_format():
    postal_code = "123"
    result = validate_dutch_postal_code(postal_code)
    assert result["status"] == "error"
    assert "Invalid Format" in result["message"]


def test_none_postal_code():
    postal_code = None
    result = validate_dutch_postal_code(postal_code)
    assert result["status"] == "error"
    assert "Invalid Input Type" in result["message"]


def test_postal_code_without_space():
    postal_code = "6000AA"
    result = validate_dutch_postal_code(postal_code)
    assert result["status"] == "success"
