# app.py
import sqlite3
from flask import Flask, request, jsonify
from postal_validator import validate_dutch_postal_code
from data_layer import get_all_prefixes, add_prefix, delete_prefix, get_prefix
from database import init_db

app = Flask(__name__)

# Initialize the database when the app starts
init_db()


# This is the original validation endpoint, now with improved error handling.
@app.route("/validate", methods=["POST"])
def validate_parcel_code():
    data = request.get_json()

    if not data or "postal_code" not in data:
        # Return a 400 status code for a bad request
        return (
            jsonify(
                {"status": "error", "message": "Missing 'postal_code' in request body."}
            ),
            400,
        )

    postal_code = data["postal_code"]

    # We get a result with a status and a message from the business logic.
    result = validate_dutch_postal_code(postal_code)

    # Now we handle different status codes based on the result.
    if result["status"] == "error":
        # Invalid format or input type is a bad request from the client.
        return jsonify(result), 400
    elif result["status"] == "warning":
        # Non-standard area is still a successful validation, but with a warning.
        return jsonify(result), 200
    else:
        # Success is a successful validation.
        return jsonify(result), 200


# The CRUD endpoint for managing postal prefixes.
@app.route("/postal_prefixes", methods=["GET", "POST"])
def handle_prefixes():
    if request.method == "GET":
        # Read: Get all prefixes
        prefixes = get_all_prefixes()
        return jsonify(prefixes)
    elif request.method == "POST":
        # Create: Add a new prefix
        data = request.get_json()
        prefix = data.get("prefix")
        if not prefix:
            return jsonify({"error": "Missing 'prefix' in request body."}), 400

        try:
            add_prefix(prefix)
            return jsonify({"message": f"Prefix {prefix} added successfully."}), 201
        except sqlite3.IntegrityError:
            # Handle case where the prefix already exists
            return jsonify({"error": f"Prefix {prefix} already exists."}), 409
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route("/postal_prefixes/<prefix>", methods=["DELETE"])
def delete_prefix_by_param(prefix):
    # Delete: Remove a specific prefix
    existing_prefix = get_prefix(prefix)
    if not existing_prefix:
        return jsonify({"error": f"Prefix {prefix} not found."}), 404

    try:
        delete_prefix(prefix)
        return jsonify({"message": f"Prefix {prefix} deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
