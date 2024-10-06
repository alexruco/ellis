# db_connector.py

import sqlite3

# Define the path for the SQLite database
DB_NAME = 'instance.db'

def init_db():
    """
    Initialize the SQLite database and create necessary tables if they don't exist.
    Ensure the database file is created if it doesn't already exist.
    Tables:
    - emails: Stores the email metadata (sender, recipient, subject, body, email_hash).
    - processed_emails: Stores email hashes to track which emails have been processed.
    """
    # Check if the database file exists, and create it if necessary
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Create the emails table to store email details
    c.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            recipient TEXT NOT NULL,
            subject TEXT,
            body TEXT,
            email_hash VARCHAR(128) UNIQUE NOT NULL
        )
    ''')

    # Create the processed_emails table to store email hashes
    # Using VARCHAR(64) to ensure the full hash is stored
    c.execute('''
        CREATE TABLE IF NOT EXISTS processed_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_hash VARCHAR(64) UNIQUE NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def get_connection():
    """
    Establish and return a connection to the SQLite database.
    """
    return sqlite3.connect(DB_NAME)
