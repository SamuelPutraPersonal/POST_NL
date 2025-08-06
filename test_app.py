# test_app.py
import pytest

# We import our Flask application object from app.py
from app import app as flask_app


# This is a pytest "fixture". It sets up a special client that can send
# requests directly to our Flask app without needing to run a real server.
# It's great for fast, isolated API testing.
@pytest.fixture
def client():
    # 'with' statement ensures the test client is properly set up and cleaned up.
    with flask_app.test_client() as client:
        yield client  # 'yield' means the code after this will run after the test finishes.


def test_validate_standard_postal_code_api(client):
    """
    Test Case 1: API Happy Path - Send a valid, standard postal code to the API.
    Check if the API returns the correct success status and message.
    """
    # Send a POST request to '/validate' with JSON data
    response = client.post("/validate", json={"postal_code": "1012 AB"})
    # Assert that the HTTP status code is 200 (OK)
    assert response.status_code == 200
    # Assert that the JSON response body is exactly what we expect
    assert response.json == {"status": "success", "message": "Standard Delivery"}
    print(f"API Test Passed: Standard postal code returned correct response.")


def test_validate_non_standard_postal_code_api(client):
    """
    Test Case 2: API Negative Path - Send a valid but non-standard postal code.
    Check if the API returns the correct warning.
    """
    response = client.post("/validate", json={"postal_code": "9999 ZZ"})
    assert response.status_code == 200
    assert response.json == {
        "status": "warning",
        "message": "Special Handling (Non-Standard Area)",
    }
    print(f"API Test Passed: Non-standard postal code returned correct warning.")


def test_validate_invalid_format_postal_code_api(client):
    """
    Test Case 3: API Negative Path - Send an invalid format (too short).
    Check if the API returns the correct error.
    """
    response = client.post("/validate", json={"postal_code": "123"})
    assert (
        response.status_code == 200
    )  # Our API returns 200 for validation results, even errors
    assert response.json == {
        "status": "error",
        "message": "Special Handling (Invalid Format)",
    }
    print(f"API Test Passed: Invalid format postal code returned correct error.")


def test_validate_missing_postal_code_in_request_api(client):
    """
    Test Case 4: API Negative Path - Send a request with missing 'postal_code' key.
    Check if the API returns a 400 Bad Request.
    """
    response = client.post("/validate", json={"some_other_key": "1234 AB"})
    assert (
        response.status_code == 400
    )  # This is an HTTP error, so status code is different
    assert response.json == {
        "status": "error",
        "message": "Missing 'postal_code' in request body.",
    }
    print(f"API Test Passed: Missing postal code in request returned 400 error.")


def test_validate_none_postal_code_api(client):
    """
    Test Case 5: API Edge Case - Send a None value for postal code.
    Check if the API returns the correct error.
    """
    response = client.post("/validate", json={"postal_code": None})
    assert (
        response.status_code == 200
    )  # Our API returns 200 for validation results, even errors
    assert response.json == {
        "status": "error",
        "message": "Special Handling (Invalid Input Type)",
    }
    print(f"API Test Passed: None postal code returned correct error.")
