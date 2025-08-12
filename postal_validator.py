# postal_validator.py

import re
from data_layer import get_all_prefixes

POSTAL_CODE_REGEX = re.compile(r"^\d{4}\s?[A-Za-z]{2}$")


def validate_dutch_postal_code(postal_code: str) -> dict:
    """
    This function takes a postal code and decides if it's for standard delivery
    or needs special handling.
    """
    if not isinstance(postal_code, str):
        return {"status": "error", "message": "Special Handling (Invalid Input Type)"}

    if not POSTAL_CODE_REGEX.match(postal_code.upper()):
        return {"status": "error", "message": "Special Handling (Invalid Format)"}

    # IMPORTANT CHANGE: We get the full list of prefixes from the data layer.
    standard_prefixes = get_all_prefixes()
    numeric_part = postal_code[:4]

    if numeric_part[:2] in standard_prefixes:
        return {"status": "success", "message": "Standard Delivery"}
    else:
        return {"status": "warning", "message": "Special Handling (Non-Standard Area)"}
