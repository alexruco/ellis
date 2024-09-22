# main.py

from db_connector import init_db
from emails_handler import handle_incoming_email
from conversation_handler import search_email_history
from josephroulin import receive_emails  # Import the email retrieval function
from get_env import USERNAME, PASSWORD, IMAP_SERVER  # Import credentials and server info

def get_history(email_address):
    """
    Retrieves and displays the email history for a specific email address.

    Args:
        email_address (str): The email address to search for.
    """
    # Ensure the database is initialized
    init_db()
    
    # Search email history based on the provided email address
    email_history = search_email_history(email_address)

    # Display the search results
    if email_history:
        print(f"Email history found for {email_address}:")
        for email in email_history:
            print(f"From: {email[0]}, To: {email[1]}, Subject: {email[2]}, Body: {email[3]}")
    else:
        print(f"No email history found for {email_address}.")

def get_incoming_messages():
    """
    Fetches incoming emails from the email server and processes them.
    """
    # Ensure the database is initialized
    init_db()

    # Step 2: Fetch emails from the email server using the receive_emails function
    try:
        print(USERNAME, PASSWORD, IMAP_SERVER)
        email_data_list = receive_emails(USERNAME, PASSWORD, IMAP_SERVER)
        # Step 3: Process each email
        for email_data in email_data_list:
            handle_incoming_email(email_data)

    except Exception as e:
        print(f"Error while fetching emails: {str(e)}")

if __name__ == "__main__":
    #get_incoming_messages()  # Fetch and process incoming emails
    get_history("alex@ruco.pt")  # Example: Get history for a specific email
