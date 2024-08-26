#append_messages.py
from utils import extract_email_address
from datetime import datetime

def append_to_conversation_history(email, conv_key, pool):
    insert_query = """
        INSERT INTO tb_conversation_history (sender, recipient, sender_type, content, timestamp, attachment, conv_key)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    sender = extract_email_address(email["email"]["from"])
    recipient = extract_email_address(email["email"]["to"])
    content = email["email"]["body"]
    timestamp = datetime.now()
    attachment = None  
    sender_type = "user" if sender in recipient else "system"
    
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(insert_query, (sender, recipient, sender_type, content, timestamp, attachment, conv_key))
            conn.commit()
    finally:
        pool.putconn(conn)

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
