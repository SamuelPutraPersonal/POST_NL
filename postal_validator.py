# postal_validator.py
import re

# This is a "regular expression" pattern.
# It tells Python exactly what a valid Dutch postal code format looks like:
# ^\d{4}   : Starts with exactly 4 digits (e.g., 1234)
# \s?      : Optionally, has a single space (e.g., 1234 AB or 1234AB)
# [A-Za-z]{2}$ : Ends with exactly 2 letters (case-insensitive)
POSTAL_CODE_REGEX = re.compile(r"^\d{4}\s?[A-Za-z]{2}$")

# This is a set (like a list, but faster for checking if something is "in" it)
# of the first two digits of postal codes that PostNL considers "standard" delivery areas.
# Any other first two digits will be considered "non-standard" for this simplified example.
STANDARD_POSTAL_CODE_PREFIXES = {
    "10",
    "11",
    "20",
    "25",
    "30",
    "35",
    "40",
    "50",
    "60",
    "70",
    "80",
    "90",
}


def validate_dutch_postal_code(postal_code: str) -> dict:
    """
    This function takes a postal code and decides if it's for standard delivery
    or needs special handling. It returns a dictionary with a 'status' and 'message'.
    This is what our API will send back.
    """
    # Step 1: Check if the input is actually a string.
    # If someone sends us a number or nothing, that's an immediate error.
    if not isinstance(postal_code, str):
        return {"status": "error", "message": "Special Handling (Invalid Input Type)"}

    # Step 2: Check the format of the postal code using our regex.
    # We convert it to uppercase first to handle "ab" vs "AB" consistently.
    if not POSTAL_CODE_REGEX.match(postal_code.upper()):
        return {"status": "error", "message": "Special Handling (Invalid Format)"}

    # Step 3: If the format is correct, now check if it's a "standard" area.
    # We take the first 4 digits (e.g., "1012" from "1012 AB")
    numeric_part = postal_code[:4]
    # Then we take the first 2 digits of that (e.g., "10")
    if numeric_part[:2] in STANDARD_POSTAL_CODE_PREFIXES:
        return {"status": "success", "message": "Standard Delivery"}
    else:
        # If the first two digits are not in our "standard" list
        return {"status": "warning", "message": "Special Handling (Non-Standard Area)"}


# IMPORTANT: We removed the `if __name__ == "__main__":` block from here.
# This file is now purely a "library" that other files (like our API and tests) will use.
