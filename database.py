# database.py

import sqlite3

DATABASE_FILE = "postal_prefixes.db"


def init_db():
    """
    Initializes the SQLite database and creates the postal_prefixes table.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS postal_prefixes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prefix TEXT NOT NULL UNIQUE
        )
    """
    )

    # Populate with initial data if the table is empty
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
    try:
        cursor.executemany(
            "INSERT INTO postal_prefixes (prefix) VALUES (?)", initial_prefixes
        )
        conn.commit()
    except sqlite3.IntegrityError:
        # This error occurs if the prefixes already exist (due to the UNIQUE constraint)
        # We can safely ignore it, as it just means the data is already there.
        pass

    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized and populated.")
