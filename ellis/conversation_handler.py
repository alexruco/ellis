# conversation_handler.py

from emails_handler import append_to_conversation_history, extract_email_address, extract_conversation_key

def check_and_process_conversation_key(email, pool):
    sender = extract_email_address(email["email"]["from"])
    subject = email["email"]["subject"]

    # Step 1: Extract conversation key from the subject
    conversation_key = extract_conversation_key(subject)

    if conversation_key:
        print(f"Conversation key found: {conversation_key}. Proceeding to check for conversation history.")
        # Step 2: Check for existing conversation history
        conversation_history = retrieve_conversation_history(conversation_key, pool)

        # Step 3: Append the email to the conversation history
        append_to_conversation_history(email, conversation_key, pool)

        # Step 4: Print or handle the conversation history
        if conversation_history:
            print("Conversation history found and updated.")
            return conversation_history
        else:
            print(f"No active conversation found for key: {conversation_key} and sender: {sender}. New conversation started.")
            return None
    else:
        print(f"No conversation key found in the subject: {subject}")

    return None

def check_active_conversation_existence(conversation_key, sender, pool):
    """
    Check if a conversation exists for the given conversation key and sender.
    """
    # Extract just the email address for checking
    sender_email = extract_email_address(sender)
    
    query = """
        SELECT conv_key 
        FROM tb_conversation 
        WHERE conv_key = %s
        AND (
            user_email ILIKE ANY(ARRAY[%s]) 
            OR system_email ILIKE ANY(ARRAY[%s])
            OR model_email ILIKE ANY(ARRAY[%s])
        ) 
        AND active_service = TRUE;
    """
    
    emails_to_check = [f"%{sender_email.strip()}%"]

    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(query, (conversation_key, emails_to_check, emails_to_check, emails_to_check))
            result = cur.fetchone()
            return bool(result)
    finally:
        pool.putconn(conn)

def check_conversation_existence(conv_key, pool):
    query = """
        SELECT 1 FROM tb_conversation WHERE conv_key = %s;
    """
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(query, (conv_key,))
            result = cur.fetchone()
            return bool(result)
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
