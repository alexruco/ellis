#get_messages.py

from josephroulin import receive_emails
from config import USERNAME, PASSWORD, IMAP_SERVER
from db_connector import init_db_pool, close_all_connections, get_db_pool

# Initialize the connection pool
init_db_pool()

# Retrieve the connection pool
pool = get_db_pool()

# Receive emails and get their hashes
emails_with_hashes = receive_emails(USERNAME, PASSWORD, IMAP_SERVER)

def filter_unprocessed_emails(emails_with_hashes, pool):
    """
    Takes a list of emails with their hashes, checks which ones have not been processed,
    and returns only the unprocessed emails.
    """
    # Extract the hashes to check for processing status
    hashes_to_check = [email["hash"] for email in emails_with_hashes]

    # Query the database to get processed hashes
    query = """
        SELECT email_hash FROM tb_processed_emails WHERE email_hash = ANY(%s);
    """
    with pool.getconn() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (hashes_to_check,))
            processed_hashes = [row[0] for row in cur.fetchall()]

    # Filter out processed emails
    unprocessed_emails = [email for email in emails_with_hashes if email["hash"] not in processed_hashes]

    return unprocessed_emails

# Filter out processed emails using the pool
unprocessed_emails = filter_unprocessed_emails(emails_with_hashes, pool)

# (Optional) Print unprocessed emails or perform further processing
for email_data in unprocessed_emails:
    print(f"Date: {email_data['email']['date']}")
    print(f"From: {email_data['email']['from']}")
    print(f"To: {email_data['email']['to']}")
    print(f"Subject: {email_data['email']['subject']}")
    print(f"Body: {email_data['email']['body']}")
    print(f"Hash: {email_data['hash']}\n")

# Close all connections when done
close_all_connections()
