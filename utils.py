# utils.py

import hashlib
import re

def extract_email_address(full_address):
    """
    Extracts the actual email address from a full address string.
    
    Example:
    Input: "Alex Ruco <alex@ruco.pt>"
    Output: "alex@ruco.pt"

    Args:
        full_address (str): The full email address, possibly including a name.

    Returns:
        str: The extracted email address.
    """
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', full_address)
    return email_match.group(0) if email_match else full_address

def is_valid_email(email_address):
    """
    Checks if an email address is valid based on a flexible regex pattern.

    Args:
        email_address (str): The email address to validate.

    Returns:
        bool: True if the email address is valid, False otherwise.
    """
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email_address) is not None

def generate_email_hash(email):
    """
    Generates a unique hash for an email based on its content.
    
    Args:
        email (dict): The email data containing sender, recipient, subject, and body.
    
    Returns:
        str: A unique hash string for the email.
    """
    email_data = f"{email['email']['from']}-{email['email']['to']}-{email['email']['subject']}-{email['email']['body']}"
    return hashlib.sha256(email_data.encode('utf-8')).hexdigest()

def sanitize_text(text):
    """
    Sanitizes a given text string by trimming whitespace and converting to lowercase.
    
    Args:
        text (str): The text to sanitize.
    
    Returns:
        str: The sanitized string.
    """
    return text.strip().lower()

def extract_domain(email_address):
    """
    Extracts the domain from an email address.
    
    Args:
        email_address (str): The email address from which to extract the domain.
    
    Returns:
        str: The domain part of the email address.
    """
    return email_address.split('@')[-1] if '@' in email_address else None
