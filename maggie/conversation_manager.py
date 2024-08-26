# conversation_manager.py

import re
from db_connector import get_db_connection
from datetime import datetime

# Extract the email address from a string
def extract_email_address(email_string):
    match = re.search(r'[\w\.-]+@[\w\.-]+', email_string)
    return match.group(0) if match else None

def retrieve_conversation_history(email, pool):
    sender = extract_email_address(email["email"]["from"])
    recipient = extract_email_address(email["email"]["to"])

    # Prepare the emails to check
    emails_to_check = [f"%{email_addr.strip()}%" for email_addr in [sender, recipient]]

    # Construct the actual SQL query string for debugging
    actual_query = f"""
        SELECT conv_key 
        FROM tb_conversation 
        WHERE (user_email ILIKE ANY(ARRAY{emails_to_check}) OR system_email ILIKE ANY(ARRAY{emails_to_check})) 
        AND active_service = TRUE;
    """

    # Print the query string for debugging
    #print("SQL Query to Execute:")
    #print(actual_query)

    conv_key = None
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT conv_key FROM tb_conversation WHERE (user_email ILIKE ANY(%s) OR system_email ILIKE ANY(%s)) AND active_service = TRUE;",
                (emails_to_check, emails_to_check)
            )
            result = cur.fetchone()
            if result:
                conv_key = result[0]
                print(f"Conversation key found: {conv_key}")
            else:
                print(f"No conversation found for email. Subject: {email['email']['subject']}, Sender: {email['email']['from']}")

        if conv_key:
            print(f"I found a conv_key! {conv_key}")
            append_to_conversation_history(email, conv_key, pool)

            history_query = """
                SELECT sender, recipient, sender_type, content, timestamp, attachment 
                FROM tb_conversation_history 
                WHERE conv_key = %s 
                ORDER BY timestamp ASC;
            """
            with conn.cursor() as cur:
                cur.execute(history_query, (conv_key,))
                conversation_history = cur.fetchall()
                return conversation_history
    finally:
        pool.putconn(conn)

    return None

# conversation_manager.py

from db_connector import get_db_connection
from datetime import datetime

def append_to_conversation_history(email, conv_key, pool):
    insert_query = """
        INSERT INTO tb_conversation_history (sender, recipient, sender_type, content, timestamp, attachment, conv_key)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    sender = email["email"]["from"]
    recipient = email["email"]["to"]
    content = email["email"]["body"]
    timestamp = datetime.now() 
    attachment = None  

    # You may need to revise this logic based on your requirements
    sender_type = "user" if any(sender == addr.strip() for addr in recipient.split(',')) else "system"
    
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(insert_query, (sender, recipient, sender_type, content, timestamp, attachment, conv_key))
            conn.commit()  # Make sure to commit the transaction
            print(f"Inserted email into conversation history with conv_key: {conv_key}")
    except Exception as e:
        print(f"Error inserting into conversation history: {e}")
    finally:
        pool.putconn(conn)
