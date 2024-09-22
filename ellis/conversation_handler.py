# conversation_handler_sqlite.py

from db_connector import get_connection
from utils import extract_email_address  # Import email extraction function

def process_email(email):
    """
    Processes an email by saving its details into the database and marking it as processed.

    Args:
        email (dict): The email data containing sender, recipient, subject, body, and hash.
    """
    # Extract the actual email addresses from the full addresses
    sender = extract_email_address(email["email"]["from"])
    recipient = extract_email_address(email["email"]["to"])
    subject = email["email"]["subject"]
    body = email["email"]["body"]
    email_hash = email["hash"]

    # Connect to the SQLite database
    conn = get_connection()
    c = conn.cursor()

    # Insert the email details into the emails table, avoid duplicate entries with the same hash
    insert_query = '''
        INSERT INTO emails (sender, recipient, subject, body, email_hash)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(email_hash) DO NOTHING
    '''
    
    # Execute the insertion query with the extracted email addresses
    c.execute(insert_query, (sender, recipient, subject, body, email_hash))
    
    # Commit the changes
    conn.commit()

    # Mark the email as processed by adding its hash to processed_emails
    append_to_processed_emails(email_hash)

    # Close the database connection
    conn.close()

def append_to_processed_emails(email_hash):
    """
    Appends an email hash to the processed_emails table to mark it as processed.

    Args:
        email_hash (str): The hash of the email to be marked as processed.
    """
    conn = get_connection()
    c = conn.cursor()

    # Insert the email hash into the processed_emails table (ignore if it already exists)
    insert_query = 'INSERT OR IGNORE INTO processed_emails (email_hash) VALUES (?)'
    
    # Execute the query
    c.execute(insert_query, (email_hash,))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def search_email_history(email_address):
    """
    Searches for emails in the database where the given email address appears as either the sender or recipient.

    Args:
        email_address (str): The email address to search for.

    Returns:
        list of tuples: A list of email records (sender, recipient, subject, body) where the address was involved.
    """
    # Connect to the SQLite database
    conn = get_connection()
    c = conn.cursor()

    # Query to find emails where the given address is either the sender or recipient
    search_query = '''
        SELECT sender, recipient, subject, body 
        FROM emails 
        WHERE sender = ? OR recipient = ?
    '''

    # Execute the query
    c.execute(search_query, (email_address, email_address))
    email_history = c.fetchall()

    # Close the database connection
    conn.close()

    return email_history
