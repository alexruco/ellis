# conversation_history_handler.py

from datetime import datetime

def append_to_conversation_history(email, conv_key, pool):
    """
    Append the email data to the conversation history.
    """
    insert_query = """
        INSERT INTO tb_conversation_history (sender, recipient, sender_type, content, timestamp, attachment, conv_key, email_hash)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    sender = email["email"]["from"]
    recipient = email["email"]["to"]
    content = email["email"]["body"]
    timestamp = datetime.now()
    attachment = None  # This can be extended to handle attachments
    sender_type = "user" if sender in recipient else "system"
    email_hash = email["hash"]
    
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(insert_query, (sender, recipient, sender_type, content, timestamp, attachment, conv_key, email_hash))
            conn.commit()
    finally:
        pool.putconn(conn)

def retrieve_conversation_history(conversation_key, pool):
    """
    Retrieve the conversation history for a given conversation key.
    """
    query = """
        SELECT sender, recipient, sender_type, content, timestamp, attachment 
        FROM tb_conversation_history 
        WHERE conv_key = %s 
        ORDER BY timestamp ASC;
    """

    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(query, (conversation_key,))
            conversation_history = cur.fetchall()
            return conversation_history
    finally:
        pool.putconn(conn)
