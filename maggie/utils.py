#utils.py

import re

def extract_email_address(full_email):
    match = re.search(r'[\w\.-]+@[\w\.-]+', full_email)
    return match.group(0) if match else None

def extract_conversation_key(subject):
    match = re.search(r'conversation:(\w+)', subject)
    return match.group(1) if match else None
