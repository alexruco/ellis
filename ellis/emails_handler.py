# ellis/emails_handler.py
from ellis.utils import extract_email_address, generate_email_hash, is_valid_email, normalize_hash
from ellis.conversation_handler import process_email
import os
from ellis.db_connector import get_connection


def filter_unprocessed_emails(emails_with_hashes):
    """
    Filters out emails that have not been processed based on the first 6 characters of their hash.

    Args:
        emails_with_hashes (list of dict): List of emails, each containing a 'hash' key.

    Returns:
        list of dict: List of unprocessed emails.
    """
    # Get the first 6 characters of the normalized hashes
    hashes_to_check = [normalize_hash(email["hash"])[:6] for email in emails_with_hashes]
    print(f"Hashes recém-gerados (primeiros 6 caracteres): {hashes_to_check}")

    if not hashes_to_check:
        return []

    conn = get_connection()
    db_path = os.path.abspath('instance.db')
    print(f"Conectado ao banco de dados: {db_path}")
    c = conn.cursor()

    try:
        # Retrieve all stored hashes, normalize them, and take the first 6 characters
        c.execute("SELECT email_hash FROM processed_emails")
        rows = c.fetchall()
        print(f"Number of hashes retrieved from the database: {len(rows)}")
        print(f"Rows retrieved: {rows}")

        # Handle potential None values and normalize
        stored_hashes = [normalize_hash(row[0])[:6] for row in rows if row[0] is not None]
        print(f"Stored hashes (first 6 characters): {stored_hashes}")

        # Using a set for faster lookup
        stored_hashes_set = set(stored_hashes)
        print(f"Stored hashes set: {stored_hashes_set}")

        # Identify processed hashes based on the first 6 characters
        processed_hashes = [h for h in hashes_to_check if h in stored_hashes_set]

        print(f"Hashes que já existem no banco (primeiros 6 caracteres): {processed_hashes}")

        # Filter out processed emails based on the first 6 characters of their hash
        
        for dbug_email in emails_with_hashes:
            print(f'normalize_hash(email["hash"])[:6]{normalize_hash(dbug_email["hash"])[:6]}')
        
        unprocessed_emails = [
            email for email in emails_with_hashes
            if normalize_hash(email["hash"])[:6] not in stored_hashes_set
        ]

        print(f"Hashes dos emails que serão processados: {[email['hash'] for email in unprocessed_emails]}")

    except Exception as e:
        print(f"An error occurred while processing hashes: {e}")
        unprocessed_emails = []

    finally:
        conn.close()

    return unprocessed_emails

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
