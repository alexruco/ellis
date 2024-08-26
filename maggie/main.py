# main.py

from email_processor import receive_emails
from db_connector import init_db_pool, close_all_connections, get_db_pool
from conversation_handler import extract_conversation_key, check_conversation_existence
from conversation_history_handler import ( 
    append_to_conversation_history, 
    retrieve_conversation_history
)
from append_messages import append_to_processed_emails
from config import USERNAME, PASSWORD, IMAP_SERVER

def main():
    # Initialize DB connection pool
    init_db_pool()
    
    # Retrieve the connection pool
    pool = get_db_pool()
    if pool is None:
        print("Failed to initialize the database connection pool. Exiting.")
        return
    
    # Step 1: Retrieve emails
    emails_with_hashes = receive_emails(USERNAME, PASSWORD, IMAP_SERVER)

    # Step 2: Process each email
    for email_data in emails_with_hashes:
        subject = email_data['email']['subject']
        sender = email_data['email']['from']
        email_hash = email_data['hash']

        # Step 3: Extract conversation key from the subject
        conversation_key = extract_conversation_key(subject)
        print(f"Processing email with hash {email_hash}, from {sender} with the subject {subject} ")

        if conversation_key:
            print(f"Conversation key found: {conversation_key}. Checking conversation existence.")
            
            # Step 4: Check if the conversation key exists and sender is part of an active conversation
            conversation_exists = check_conversation_existence(conversation_key, sender, pool)
            
            if conversation_exists:
                # Step 5: Append the email to the conversation history
                append_to_conversation_history(email_data, conversation_key, pool)
                
                # Step 6: Retrieve and print the conversation history
                conversation_history = retrieve_conversation_history(conversation_key, pool)
                if conversation_history:
                    print("Conversation history found and updated.")
                else:
                    print(f"No history found for key: {conversation_key}.")
            else:
                print(f"No active conversation found for key: {conversation_key} and sender: {sender}.")
        else:
            print(f"No active conversation for email from {sender} with the subject {subject} ")

        # Step 7: Append the email hash to processed emails
        append_to_processed_emails(email_hash, pool)

    # Close DB connections
    close_all_connections()

if __name__ == "__main__":
    main()
