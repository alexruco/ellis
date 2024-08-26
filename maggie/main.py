from email_processor import receive_emails, filter_unprocessed_emails
from conversation_manager import retrieve_conversation_history
from db_connector import init_db_pool, close_all_connections, get_db_pool
from config import USERNAME, PASSWORD, IMAP_SERVER

def main():
    init_db_pool()
    pool = get_db_pool()

    emails_with_hashes = receive_emails(USERNAME, PASSWORD, IMAP_SERVER)

    unprocessed_emails = filter_unprocessed_emails(emails_with_hashes, pool)

    for email_data in unprocessed_emails:
        conversation_history = retrieve_conversation_history(email_data, pool)
        if conversation_history:
            print("Conversation History Found:")
            for entry in conversation_history:
                print(entry)
        else:
            print("No conversation found for this email.")

    close_all_connections()

if __name__ == "__main__":
    main()
