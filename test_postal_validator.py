# test_postal_validator.py

import pytest

# We import the function we want to test from our postal_validator.py file
from postal_validator import validate_dutch_postal_code, STANDARD_POSTAL_CODE_PREFIXES

# --- Test Automation (QA Perspective using pytest) ---

# pytest automatically finds functions that start with 'test_'


def test_standard_postal_code_valid():
    """
    Test Case 1: Happy Path - Verify a standard, valid postal code returns "Standard Delivery".
    """
    postal_code = "1012 AB"  # Example: Amsterdam postal code, starts with "10"
    result = validate_dutch_postal_code(postal_code)
    # 'assert' is how pytest checks if something is true. If it's false, the test fails.
    assert result == {
        "status": "success",
        "message": "Standard Delivery",
    }, f"Expected 'Standard Delivery' for {postal_code}, but got '{result}'"
    print(f"Test Passed: {postal_code} routed to Standard Delivery.")


def test_another_standard_postal_code_valid():
    """
    Test Case 2: Happy Path - Verify another standard, valid postal code returns "Standard Delivery".
    """
    postal_code = "6000 AA"  # Example: Limburg postal code, starts with "60"
    result = validate_dutch_postal_code(postal_code)
    assert result == {
        "status": "success",
        "message": "Standard Delivery",
    }, f"Expected 'Standard Delivery' for {postal_code}, but got '{result}'"
    print(f"Test Passed: {postal_code} routed to Standard Delivery.")


def test_non_standard_postal_code_numeric_prefix():
    """
    Test Case 3: Negative Path - Verify a postal code with a non-standard numeric prefix returns "Special Handling".
    """
    postal_code = (
        "0123 AB"  # Starts with "01", not in our STANDARD_POSTAL_CODE_PREFIXES
    )
    result = validate_dutch_postal_code(postal_code)
    assert result == {
        "status": "warning",
        "message": "Special Handling (Non-Standard Area)",
    }, f"Expected 'Special Handling' for {postal_code}, but got '{result}'"
    print(f"Test Passed: {postal_code} routed to Special Handling (Non-Standard Area).")


def test_invalid_short_postal_code_format():
    """
    Test Case 4: Negative Path - Verify an invalid (too short) postal code format returns "Special Handling".
    """
    postal_code = "123"
    result = validate_dutch_postal_code(postal_code)
    assert result == {
        "status": "error",
        "message": "Special Handling (Invalid Format)",
    }, f"Expected 'Special Handling (Invalid Format)' for {postal_code}, but got '{result}'"
    print(f"Test Passed: {postal_code} routed to Special Handling (Invalid Format).")


def test_empty_postal_code():
    """
    Test Case 5: Edge Case - Verify an empty string postal code returns "Special Handling".
    """
    postal_code = ""
    result = validate_dutch_postal_code(postal_code)
    assert result == {
        "status": "error",
        "message": "Special Handling (Invalid Format)",
    }, f"Expected 'Special Handling (Invalid Format)' for empty string, but got '{result}'"
    print(
        f"Test Passed: Empty postal code routed to Special Handling (Invalid Format)."
    )


def test_none_postal_code():
    """
    Test Case 6: Edge Case - Verify a None value for postal code returns "Special Handling".
    """
    postal_code = None
    result = validate_dutch_postal_code(postal_code)
    assert result == {
        "status": "error",
        "message": "Special Handling (Invalid Input Type)",
    }, f"Expected 'Special Handling (Invalid Input Type)' for None, but got '{result}'"
    print(
        f"Test Passed: None postal code routed to Special Handling (Invalid Input Type)."
    )


def test_long_postal_code_format():
    """
    Test Case 7: Verify a postal code that is too long (but matches regex prefix)
    now returns "Special Handling (Invalid Format)" due to the improved regex.
    """
    postal_code = "10123456789 AB"  # Too long, but starts with "10"
    result = validate_dutch_postal_code(postal_code)
    assert result == {
        "status": "error",
        "message": "Special Handling (Invalid Format)",
    }, f"Expected 'Special Handling (Invalid Format)' for {postal_code}, but got '{result}'"
    print(
        f"Test Passed: {postal_code} (long format) correctly identified as invalid format."
    )


def test_postal_code_without_space():
    """
    Test Case 8: Verify a valid postal code without a space (e.g., 1012AB) is handled.
    """
    postal_code = "1012AB"
    result = validate_dutch_postal_code(postal_code)
    assert result == {
        "status": "success",
        "message": "Standard Delivery",
    }, f"Expected 'Standard Delivery' for {postal_code}, but got '{result}'"
    print(f"Test Passed: {postal_code} (no space) routed to Standard Delivery.")
