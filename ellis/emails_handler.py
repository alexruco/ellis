# emails_handler_sqlite.py

from ellis.db_connector import get_connection
from ellis.utils import extract_email_address, generate_email_hash, is_valid_email
from ellis.conversation_handler import process_email

def handle_incoming_email(email_data):
    """
    Handles an incoming email by processing it and storing it in the database,
    then retrieves the email history of the sender.

    Args:
        email_data (dict): The email data containing sender, recipient, subject, and body.
    """
    sender_full = email_data["email"]["from"]
    recipient_full = email_data["email"]["to"]

    # Extract the actual email addresses
    sender = extract_email_address(sender_full)
    recipient = extract_email_address(recipient_full)

    # Log the sender and recipient to troubleshoot the issue
    #print(f"Processing email from {sender} to {recipient}")

    # Validate the sender and recipient emails
    if is_valid_email(sender) and is_valid_email(recipient):
        # Generate a unique hash for the email
        email_data["hash"] = generate_email_hash(email_data)

        # Process the email (store in DB and mark as processed)
        process_email(email_data)
        print(f"Email from {sender} processed successfully.")

    else:
        print(f"Invalid sender or recipient email address: {sender_full} or {recipient_full}")

def filter_unprocessed_emails(emails_with_hashes):
    """
    Filters out emails that have already been processed based on their hash.

    Args:
        emails_with_hashes (list of dict): List of emails where each email contains a 'hash' key.

    Returns:
        list of dict: List of unprocessed emails.
    """
    # Extract email hashes from the input emails
    hashes_to_check = [email["hash"] for email in emails_with_hashes]

    # If there are no emails to process, return immediately
    if not hashes_to_check:
        return []

    # Connect to the SQLite DB
    conn = get_connection()
    c = conn.cursor()

    # Query to check if the email hash exists in the processed_emails table
    query = f'SELECT email_hash FROM processed_emails WHERE email_hash IN ({",".join("?" * len(hashes_to_check))})'
    
    # Execute the query with the list of hashes to check
    c.execute(query, hashes_to_check)
    processed_hashes = [row[0] for row in c.fetchall()]

    conn.close()

    # Filter out emails whose hash is in the processed_hashes list
    unprocessed_emails = [email for email in emails_with_hashes if email["hash"] not in processed_hashes]
    
    return unprocessed_emails
