# ellis/main.py

from ellis.db_connector import init_db
from ellis.emails_handler import handle_incoming_email
from ellis.conversation_handler import search_email_history

from josephroulin import receive_emails  # Import the email retrieval function
from ellis.get_env import get_username, get_password, get_imap_server  # Use getter functions for dynamic variable fetching

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

def get_new_messages():
    """
    Fetches incoming emails from the email server and processes them.
    """
    # Ensure the database is initialized
    init_db()

    # Step 1: Dynamically fetch the environment variables using getter functions
    username = get_username()
    password = get_password()
    imap_server = get_imap_server()

    # Step 2: Print for verification (optional)
    print(f"Using EMAIL_USERNAME: {username}, EMAIL_PASSWORD: {password}, IMAP_SERVER: {imap_server}")

    # Step 3: Fetch emails from the email server using the receive_emails function
    try:
        email_data_list = receive_emails(username, password, imap_server)
        # Step 4: Process each email
        for email_data in email_data_list:
            handle_incoming_email(email_data)

    except Exception as e:
        print(f"Error while fetching emails: {str(e)}")

if __name__ == "__main__":
    # Uncomment to fetch and process incoming emails
    # get_new_messages()
    
    # Example: Get history for a specific email
    get_history("alex@ruco.pt")
