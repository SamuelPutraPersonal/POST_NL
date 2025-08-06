# app.py
from flask import Flask, request, jsonify

# We import our validation logic from the postal_validator.py file
from postal_validator import validate_dutch_postal_code

# Create a Flask web application
app = Flask(__name__)


# This is an "API endpoint" or "route".
# It means when someone sends a POST request to '/validate' URL of our server,
# the function below (@app.route) will run.
@app.route("/validate", methods=["POST"])
def validate_parcel_code():
    # Try to get JSON data from the incoming request body
    data = request.get_json()

    # Check if we actually received JSON data and if it contains a 'postal_code'
    if not data or "postal_code" not in data:
        # If not, send back an error message with a 400 Bad Request status code
        return (
            jsonify(
                {"status": "error", "message": "Missing 'postal_code' in request body."}
            ),
            400,
        )

    # Get the postal code from the received data
    postal_code = data["postal_code"]

    # Call our validation logic from postal_validator.py
    result = validate_dutch_postal_code(postal_code)

    # Send the result back as a JSON response with a 200 OK status code
    return jsonify(result), 200


# This block tells Flask to run our web server when you execute this file directly.
# host='0.0.0.0' makes it accessible from outside the container (important for Docker).
# port=5000 is the port number our API will listen on.
# debug=True is useful for development, showing errors in the browser.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
