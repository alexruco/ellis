#emails_hanlder.py
from datetime import datetime
import re


def filter_unprocessed_emails(emails_with_hashes, pool):
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

def append_to_processed_emails(email_hash, pool):
    # Check if the hash already exists
    check_query = """
        SELECT 1 FROM tb_processed_emails WHERE email_hash = %s;
    """
    insert_query = """
        INSERT INTO tb_processed_emails (email_hash)
        VALUES (%s);
    """
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            # Check if the hash exists
            cur.execute(check_query, (email_hash,))
            exists = cur.fetchone()

            if not exists:
                # If the hash doesn't exist, insert it
                cur.execute(insert_query, (email_hash,))
                conn.commit()
            else:
                print(f"Email with hash {email_hash} has already been processed.")
    finally:
        pool.putconn(conn)

def append_to_conversation_history(email, conv_key, pool):
    """
    Append the email data to the conversation history.
    """
    insert_query = """
        INSERT INTO tb_conversation_history (sender, recipient, sender_type, content, timestamp, attachment, conv_key, email_hash)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    sender = email["email"]["from"]
    sender_email = extract_email_address(sender)
    recipient = email["email"]["to"]
    body = email["email"]["body"]
    content = clean_email_content(body)
    timestamp = datetime.now()
    attachment = None  # This can be extended to handle attachments
    email_hash = email["hash"]

    # Determine sender_type based on the sender's email
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT system_email, model_email
                FROM tb_conversation
                WHERE conv_key = %s
            """, (conv_key,))
            result = cur.fetchone()
            system_email, model_email = result if result else (None, None)
            
            if system_email and sender_email in system_email:
                sender_type = "system" #the message is from admin
            elif model_email and sender_email in model_email:
                sender_type = "model" #the message is from the model
            else:
                sender_type = "user" #the message is from 

            cur.execute(insert_query, (sender, recipient, sender_type, content, timestamp, attachment, conv_key, email_hash))
            conn.commit()
    finally:
        pool.putconn(conn)

def extract_email_address(full_email):
    match = re.search(r'[\w\.-]+@[\w\.-]+', full_email)
    return match.group(0) if match else None

def extract_conversation_key(subject):
    # Strip common prefixes like "Re:", "Fwd:", etc.
    clean_subject = re.sub(r"^(Re|Fwd):\s*", "", subject, flags=re.IGNORECASE)
    print(f"Cleaned Subject: {clean_subject}")  # Debugging line to see the cleaned subject
    
    # Updated to match the conversation key directly in the subject
    match = re.search(r'(\w{16})', clean_subject)  # Looking for a 16-character alphanumeric key
    if match:
        print(f"Conversation Key Found: {match.group(1)}")  # Debugging line to see the extracted key
    else:
        print("No conversation key found.")  # Debugging line if no key is found
    return match.group(1) if match else None

def clean_email_content(content):
    # Step 1: Replace \r\n with space and remove extra spaces
    content = re.sub(r'\s+', ' ', content.replace('\r\n', ' '))

    # Step 2: Remove quoted text (optional, based on "On <date> <person> wrote:" pattern)
    content = re.sub(r'On.*?wrote:.*', '', content, flags=re.DOTALL)

    # Step 3: Remove special characters like '>' used in quoted emails
    content = re.sub(r'>+', '', content)

    # Step 4: Trim leading and trailing whitespace
    content = content.strip()

    return content
