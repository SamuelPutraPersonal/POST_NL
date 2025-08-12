# data_layer.py
import sqlite3
import os
from typing import (
    Optional,
)  # Corrected import: 'list' is a built-in type and not needed here.

DB_FILE = os.path.join(os.path.dirname(__file__), "postal_prefixes.db")


def get_all_prefixes() -> list[str]:
    """
    Reads all postal prefixes from the database.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT prefix FROM postal_prefixes")
        prefixes = [row[0] for row in cursor.fetchall()]
        return prefixes
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if conn:
            conn.close()


def add_prefix(prefix: str) -> None:
    """
    Adds a new postal prefix to the database.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO postal_prefixes (prefix) VALUES (?)", (prefix,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()


def delete_prefix(prefix: str) -> None:
    """
    Deletes a postal prefix from the database.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM postal_prefixes WHERE prefix = ?", (prefix,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()


def get_prefix(prefix: str) -> Optional[str]:
    """
    Checks if a specific prefix exists in the database.
    This uses Optional[str] for compatibility with Python < 3.10.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT prefix FROM postal_prefixes WHERE prefix = ?", (prefix,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    # This block is for testing the functions directly.
    # It will not run when imported.
    print("All prefixes:", get_all_prefixes())
    test_prefix = "1011"
    result = get_prefix(test_prefix)
    if result:
        print(f"Found prefix: {result}")
    else:
        print(f"Prefix {test_prefix} not found.")
