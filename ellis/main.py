# main.py

from datetime import datetime
from josephroulin import receive_emails
from db_connector import init_db_pool, close_all_connections, get_db_pool
from conversation_handler import extract_conversation_key, check_conversation_existence, filter_unprocessed_emails
from conversation_history_handler import (
    append_to_conversation_history,
    retrieve_conversation_history
)
from append_messages import append_to_processed_emails
from get_env import USERNAME, PASSWORD, IMAP_SERVER
from utils import log_error, log_success

from db_connector import get_db_pool
from utils import log_error

def store_sent_message(conv_key, sender, recipient, content, sender_type="AI", attachment=None):

    init_db_pool()

    pool = get_db_pool()
    
    if not pool:
        log_error("Failed to retrieve the database connection pool.")
        return

    # Check if the conversation exists
    conversation_exists = check_conversation_existence_by_key(conv_key, pool)

    if not conversation_exists:
        log_error(f"Conversation with key {conv_key} does not exist. Message not stored.")
        return

    insert_query = """
        INSERT INTO tb_conversation_history (sender, recipient, sender_type, content, timestamp, attachment, conv_key)
        VALUES (%s, %s, %s, %s, NOW(), %s, %s);
    """

    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(insert_query, (sender, recipient, sender_type, content, attachment, conv_key))
            conn.commit()
            log_success(f"Message successfully stored for conversation key {conv_key}.")
    except Exception as e:
        log_error(f"Error storing message: {str(e)}")
    finally:
        pool.putconn(conn)

def check_conversation_existence_by_key(conv_key, pool):
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

def get_messages():
    # Initialize DB connection pool
    init_db_pool()
    
    # Retrieve the connection pool
    pool = get_db_pool()
    if pool is None:
        log_error("Failed to initialize the database connection pool. Exiting.")
        return
    
    # Step 1: Retrieve emails
    emails_with_hashes = receive_emails(USERNAME, PASSWORD, IMAP_SERVER)
    log_success("New emails checked.")   

    if not emails_with_hashes:
        log_success("No emails on the inbox.")
        return
    
    # Step 2: Filter out already processed emails
    unprocessed_emails = filter_unprocessed_emails(emails_with_hashes, pool)
    log_success("Unprocessed emails filtered.")

    # Step 3: Check if there are any unprocessed emails to process
    if not unprocessed_emails:
        log_success("No new emails to process.")
        return
    
    # Step 4: Process each unprocessed email
    for email_data in unprocessed_emails:
        subject = email_data['email']['subject']
        sender = email_data['email']['from']
        email_hash = email_data['hash']

        # Step 5: Extract conversation key from the subject
        conversation_key = extract_conversation_key(subject)
        log_success(f"Processing email with hash {email_hash}, from {sender} with the subject {subject}.")

        if conversation_key:
            log_success(f"Conversation key found: {conversation_key}. Checking conversation existence.")
            
            # Step 6: Check if the conversation key exists and sender is part of an active conversation
            conversation_exists = check_conversation_existence(conversation_key, sender, pool)
            log_success("Checked if conversation exists.")
            
            if conversation_exists:
                # Step 7: Append the email to the conversation history
                append_to_conversation_history(email_data, conversation_key, pool)
                log_success("Appending conversation to history.")
                
                # Step 8: Retrieve and print the conversation history
                conversation_history = retrieve_conversation_history(conversation_key, pool)
                if conversation_history:
                    log_success("Conversation history found and updated.")
                else:
                    log_success(f"No history found for key: {conversation_key}.")
            else:
                log_error(f"No active conversation found for key: {conversation_key} and sender: {sender}.")
        else:
            log_error(f"No conversation key found in the subject: {subject}.")

        # Step 9: Append the email hash to processed emails
        append_to_processed_emails(email_hash, pool)
        log_success("Mail hashes appended to processed.")

    # Close DB connections
    close_all_connections()
    return conversation_history

# Example usage of store_sent_message()

def example_store_sent_message():
    # Mock data for the sent message
    conv_key = "abcd1234efgh5670"  # Example conversation key
    sender = "ai@company.com"  # Example sender email address
    recipient = "user@example.com"  # Example recipient email address
    content = "Thank you for reaching out. How can I assist you further?"  # Example message content
    sender_type = "AI"  # Example sender type (default is "AI")
    attachment = None  # Example attachment (default is None)

    # Store the sent message in the conversation history
    store_sent_message(conv_key, sender, recipient, content, sender_type, attachment)

# Call the example function to store a message

if __name__ == "__main__":
    #get_messages()

    example_store_sent_message()
