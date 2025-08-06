# data_layer.py - The Data Layer

# This is a simple Python dictionary acting as a fake database.
# In a real application, this would be code to connect to a database like MySQL or PostgreSQL.
DATABASE = {
    "standard_postal_code_prefixes": {
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
}


def get_standard_postal_code_prefixes():
    """
    Retrieves the set of standard postal code prefixes from our "database".
    """
    return DATABASE["standard_postal_code_prefixes"]
