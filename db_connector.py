import sqlite3
from os import path

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
            email_hash TEXT UNIQUE NOT NULL
        )
    ''')

    # Create the processed_emails table to store email hashes
    c.execute('''
        CREATE TABLE IF NOT EXISTS processed_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_hash TEXT UNIQUE NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def get_connection():
    """
    Establish and return a connection to the SQLite database.
    """
    return sqlite3.connect(DB_NAME)
