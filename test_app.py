# test_app.py

import pytest
from app import app as flask_app
import os
import sqlite3

# Define the database file name
DATABASE_FILE = "postal_prefixes.db"


# Create a fixture to set up a clean database for each test
@pytest.fixture(autouse=True)
def setup_database_for_tests():
    # Remove the database file before each test to ensure a clean state
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)

    # Initialize a new, empty database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE postal_prefixes (id INTEGER PRIMARY KEY, prefix TEXT NOT NULL UNIQUE)"
    )
    initial_prefixes = [
        ("10",),
        ("11",),
        ("20",),
        ("25",),
        ("30",),
        ("35",),
        ("40",),
        ("50",),
        ("60",),
        ("70",),
        ("80",),
        ("90",),
    ]
    cursor.executemany(
        "INSERT INTO postal_prefixes (prefix) VALUES (?)", initial_prefixes
    )
    conn.commit()
    conn.close()

    yield

    # Remove the database file after each test
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)


@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client


# --- Tests for the new CRUD endpoints ---


def test_get_all_prefixes(client):
    response = client.get("/postal_prefixes")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 12  # Check if all initial prefixes are returned


def test_add_new_prefix(client):
    response = client.post("/postal_prefixes", json={"prefix": "99"})
    assert response.status_code == 201
    assert response.json["message"] == "Prefix 99 added successfully."

    # Verify the prefix was actually added
    response = client.get("/postal_prefixes")
    assert "99" in response.json


def test_add_existing_prefix_failure(client):
    response = client.post("/postal_prefixes", json={"prefix": "10"})
    assert response.status_code == 409  # Conflict
    assert "already exists" in response.json["error"]


def test_delete_prefix(client):
    response = client.delete("/postal_prefixes/10")
    assert response.status_code == 200
    assert response.json["message"] == "Prefix 10 deleted successfully."

    # Verify the prefix was deleted
    response = client.get("/postal_prefixes")
    assert "10" not in response.json


def test_delete_non_existent_prefix_failure(client):
    response = client.delete("/postal_prefixes/99")
    assert response.status_code == 404  # Not Found
    assert "not found" in response.json["error"]


# --- Tests for the updated /validate endpoint with new error codes ---


def test_validate_standard_postal_code_api(client):
    response = client.post("/validate", json={"postal_code": "1012 AB"})
    assert response.status_code == 200
    assert response.json == {"status": "success", "message": "Standard Delivery"}


def test_validate_non_standard_postal_code_api(client):
    response = client.post("/validate", json={"postal_code": "0123 AB"})
    assert response.status_code == 200
    assert response.json == {
        "status": "warning",
        "message": "Special Handling (Non-Standard Area)",
    }


def test_validate_invalid_format_postal_code_api_error_code(client):
    response = client.post("/validate", json={"postal_code": "123"})
    assert response.status_code == 400  # Now returns 400, not 200
    assert "Invalid Format" in response.json["message"]


def test_validate_none_postal_code_api_error_code(client):
    response = client.post("/validate", json={"postal_code": None})
    assert response.status_code == 400  # Now returns 400, not 200
    assert "Invalid Input Type" in response.json["message"]


def test_validate_missing_postal_code_in_request_api_error_code(client):
    response = client.post("/validate", json={"some_other_key": "1234 AB"})
    assert response.status_code == 400
    assert "Missing 'postal_code'" in response.json["message"]
