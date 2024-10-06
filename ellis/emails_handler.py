# ellis/emails_handler.py
from ellis.utils import extract_email_address, generate_email_hash, is_valid_email, normalize_hash
from ellis.conversation_handler import process_email
import os
from ellis.db_connector import get_connection

def filter_unprocessed_emails(emails_with_hashes):
    """
    Filters out emails that have already been processed based on their hash provided by Joseph Roulin.

    Args:
        emails_with_hashes (list of dict): List of emails, each containing a 'hash' key provided by Joseph Roulin.

    Returns:
        list of dict: List of unprocessed emails.
    """
    # Use the hashes provided by Joseph Roulin, taking the first 6 characters if needed
    hashes_to_check = [email["hash"][:6] for email in emails_with_hashes]
    print(f"Hashes recém-gerados (primeiros 6 caracteres): {hashes_to_check}")

    if not hashes_to_check:
        return []

    conn = get_connection()
    db_path = os.path.abspath('instance.db')
    print(f"Conectado ao banco de dados: {db_path}")
    c = conn.cursor()

    try:
        # Retrieve stored hashes from the database, which should be the Joseph Roulin hashes
        c.execute("SELECT email_hash FROM processed_emails")
        rows = c.fetchall()
        print(f"Número de hashes recuperados do banco de dados: {len(rows)}")

        # Normalize and take the first 6 characters of the stored hashes
        stored_hashes = [row[0][:6] for row in rows if row[0] is not None]
        print(f"Hashes armazenados (primeiros 6 caracteres): {stored_hashes}")

        stored_hashes_set = set(stored_hashes)

        # Identify hashes that have already been processed
        processed_hashes = [h for h in hashes_to_check if h in stored_hashes_set]
        print(f"Hashes que já existem no banco (primeiros 6 caracteres): {processed_hashes}")

        # Filter out emails whose hashes are already in the database
        unprocessed_emails = [
            email for email in emails_with_hashes
            if email["hash"][:6] not in stored_hashes_set
        ]

        print(f"Hashes dos emails que serão processados: {[email['hash'] for email in unprocessed_emails]}")

    except Exception as e:
        print(f"Ocorreu um erro ao processar os hashes: {e}")
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
