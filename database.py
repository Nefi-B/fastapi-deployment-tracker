
# Imports Python's built-in SQLite library.
import sqlite3

# Imports Path to manage file paths reliably.
from pathlib import Path


# Storing the database beside database.py. This keeps the path consistent across working directories.
DATABASE_PATH = Path(__file__).resolve().parent / "deployments.db"


# Initialize the SQLite database and create the deployments table.
def initialize_database():

    # Connect to SQLite. Create the database file if it does not exist.
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        # Create the deployments table if it does not exist. Preserve existing data.
        connection.execute("""
            CREATE TABLE IF NOT EXISTS deployments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application TEXT NOT NULL,
                version TEXT NOT NULL,
                environment TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)

        # Commit the transaction to save the table creation.
        connection.commit()

    finally:
        # Close the connection even if an error occurs.
        connection.close()

    print("Database initialized successfully!")


# Return a reusable SQLite connection for FastAPI endpoints.
def get_connection():

    # Connect to the database file.
    connection = sqlite3.connect(DATABASE_PATH)

    # Allow column access by name, such as row["application"] instead of row[1].
    connection.row_factory = sqlite3.Row

    # Return the connection. The calling function is responsible for closing it.
    return connection


# Initialize the database only when this file is executed directly.
if __name__ == "__main__":
    initialize_database()
