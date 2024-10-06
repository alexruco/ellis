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
    # Ensure the database is initialized
    init_db()
    
    # Search email history based on the provided email address
    email_history = search_email_history(email_address)

    # Format the search results into a readable string
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
    # Ensure the database is initialized
    init_db()

    # Step 1: Dynamically fetch the environment variables using getter functions
    username = get_username()
    password = get_password()
    imap_server = get_imap_server()

    # Step 2: Retrieve emails from the server
    try:
        email_data_list = receive_emails(username, password, imap_server)
        
        # Step 3: Filter out emails that have already been processed
        unprocessed_emails = filter_unprocessed_emails(email_data_list)
        
        # Step 4: Process each unprocessed email
        for email_data in unprocessed_emails:
            handle_incoming_email(email_data)

        # Step 5: Return the number of new emails processed
        return len(unprocessed_emails)

    except Exception as e:
        # If there's an error, return 0 or handle the error accordingly
        print(f"Error while fetching emails: {str(e)}")
        return 0