# ellis/main.py

from ellis.db_connector import init_db
from ellis.emails_handler import handle_incoming_email, filter_unprocessed_emails
from ellis.conversation_handler import search_email_history
from josephroulin import receive_emails
from ellis.get_env import get_username, get_password, get_imap_server

def get_history(email_address):
    """
    Retrieves and formats the email history for a specific email address.

    Args:
        email_address (str): The email address to search for.

    Returns:
        str: A formatted string representing the email history for the specified address.
    """
    init_db()
    email_history = search_email_history(email_address)
    if email_history:
        formatted_history = f"Email history found for {email_address}:\n"
        for email in email_history:
            formatted_history += f"From: {email[0]}, To: {email[1]}, Subject: {email[2]}, Body: {email[3]}\n"
    else:
        formatted_history = f"No email history found for {email_address}."
    return formatted_history

def get_new_messages():
    """
    Fetches incoming emails from the email server, filters out processed emails, and processes them.
    
    Returns:
        int: The number of new (unprocessed) emails that were successfully processed.
    """
    # Step 1: Initialize the database
    init_db()

    # Step 2: Fetch the environment variables using dynamic getters
    username = get_username()
    password = get_password()
    imap_server = get_imap_server()

    try:
        # Step 3: Retrieve emails from the server
        email_data_list = receive_emails(username, password, imap_server)

        # Step 4: Filter out already processed emails using the hash
        unprocessed_emails = filter_unprocessed_emails(email_data_list)

        # Step 5: Process each unprocessed email and track how many were newly processed
        new_emails_processed = 0  # Track newly processed emails
        for email_data in unprocessed_emails:
            handle_incoming_email(email_data)
            new_emails_processed += 1  # Increment the count for newly processed emails

        # Step 6: Return the number of newly processed emails
        return new_emails_processed

    except Exception as e:
        # If there's an error, return 0 or handle the error accordingly
        print(f"Error while fetching emails: {str(e)}")
        return 0

# Example usage in __main__ for testing
if __name__ == "__main__":
    # Get new messages and display the number of newly processed emails
    new_emails_count = get_new_messages()
    print(f"Number of new emails processed: {new_emails_count}")
