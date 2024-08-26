# conversation_handler.py

from utils import extract_email_address, extract_conversation_key
from append_messages import append_to_conversation_history, append_to_processed_emails
from conversation_history_handler import retrieve_conversation_history
def check_and_process_conversation_key(email, pool):
    sender = extract_email_address(email["email"]["from"])
    subject = email["email"]["subject"]

    # Step 1: Extract conversation key from the subject
    conversation_key = extract_conversation_key(subject)

    if conversation_key:
        print(f"Conversation key found: {conversation_key}. Proceeding to check for conversation history.")
        # Step 2: Check for existing conversation history
        conversation_history = retrieve_conversation_history(conversation_key, sender, pool)

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

def check_conversation_existence(conversation_key, sender, pool):
    """
    Check if a conversation exists for the given conversation key and sender.
    """
    query = """
        SELECT conv_key 
        FROM tb_conversation 
        WHERE conv_key = %s
        AND (
            user_email ILIKE ANY(ARRAY[%s]) 
            OR system_email ILIKE ANY(ARRAY[%s])
        ) 
        AND active_service = TRUE;
    """
    
    emails_to_check = [f"%{sender.strip()}%"]

    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(query, (conversation_key, emails_to_check, emails_to_check))
            result = cur.fetchone()
            return bool(result)
    finally:
        pool.putconn(conn)
