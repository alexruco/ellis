# ellis/conversation_handler.py

from ellis.db_connector import get_connection
from ellis.utils import extract_email_address


def process_email(email):
    """
    Processes an email by saving its details into the database and marking it as processed.

    Args:
        email (dict): The email data containing sender, recipient, subject, body, and hash.
    """
    sender = email["email"]["from"]
    recipient = email["email"]["to"]
    subject = email["email"]["subject"]
    body = email["email"]["body"]
    email_hash = email["hash"]

    print(f"Processing email with hash: {email_hash}")

    conn = get_connection()
    c = conn.cursor()

    try:
        # Begin transaction
        conn.execute('BEGIN')

        # Insert into emails table
        insert_email_query = '''
            INSERT INTO emails (sender, recipient, subject, body, email_hash)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(email_hash) DO NOTHING
        '''
        c.execute(insert_email_query, (sender, recipient, subject, body, email_hash))

        # Insert into processed_emails table
        insert_processed_query = 'INSERT OR IGNORE INTO processed_emails (email_hash) VALUES (?)'
        c.execute(insert_processed_query, (email_hash,))

        # Commit transaction
        conn.commit()

        print(f"Email with hash {email_hash} processed and marked as processed.")

    except Exception as e:
        conn.rollback()
        print(f"Error processing email with hash {email_hash}: {str(e)}")

    finally:
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
