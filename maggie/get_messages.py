#get_messages.py

from josephroulin import receive_emails
from config import USERNAME, PASSWORD, IMAP_SERVER
from db_connector import init_db_pool, close_all_connections, get_db_pool
import re

# Initialize the connection pool
init_db_pool()

# Retrieve the connection pool
pool = get_db_pool()

def extract_conversation_key(subject):
    """
    Extracts the conversation key from the email subject.
    Assumes the key is in the format [ConvKey: ABC123].
    """
    match = re.search(r'\[ConvKey: (\w+)\]', subject)
    return match.group(1) if match else None

def filter_unprocessed_emails(emails_with_hashes, pool):
    """
    Takes a list of emails with their hashes, checks which ones have not been processed,
    and returns only the unprocessed emails.
    """
    hashes_to_check = [email["hash"] for email in emails_with_hashes]
    
    query = """
        SELECT email_hash FROM tb_processed_emails WHERE email_hash = ANY(%s);
    """
    with pool.getconn() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (hashes_to_check,))
            processed_hashes = [row[0] for row in cur.fetchall()]

    unprocessed_emails = [email for email in emails_with_hashes if email["hash"] not in processed_hashes]

    return unprocessed_emails

def retrieve_conversation_history(conv_key, sender_email, pool):
    """
    Retrieves the history of emails based on the conversation key and sender email.
    """
    query = """
        SELECT * FROM tb_messages WHERE conv_key = %s AND sender_email = %s ORDER BY date ASC;
    """
    with pool.getconn() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (conv_key, sender_email))
            history = cur.fetchall()
    return history

def main():
    # Receive emails and get their hashes
    emails_with_hashes = receive_emails(USERNAME, PASSWORD, IMAP_SERVER)
    
    # Filter out processed emails
    unprocessed_emails = filter_unprocessed_emails(emails_with_hashes, pool)
    
    for email_data in unprocessed_emails:
        conv_key = extract_conversation_key(email_data['email']['subject'])
        if conv_key:
            # Retrieve conversation history
            history = retrieve_conversation_history(conv_key, email_data['email']['from'], pool)
            if history:
                print(f"Conversation history for {conv_key} and {email_data['email']['from']}:\n{history}")
            else:
                print(f"No previous history found for conversation key {conv_key}.")
        
        print(f"Date: {email_data['email']['date']}")
        print(f"From: {email_data['email']['from']}")
        print(f"To: {email_data['email']['to']}")
        print(f"Subject: {email_data['email']['subject']}")
        print(f"Body: {email_data['email']['body']}")
        print(f"Hash: {email_data['hash']}\n")

# Close all connections when done
close_all_connections()

if __name__ == "__main__":
    main()
