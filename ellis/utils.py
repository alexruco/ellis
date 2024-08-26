#utils.py

import re

def extract_email_address(full_email):
    match = re.search(r'[\w\.-]+@[\w\.-]+', full_email)
    return match.group(0) if match else None

def extract_conversation_key(subject):
    # Strip common prefixes like "Re:", "Fwd:", etc.
    clean_subject = re.sub(r"^(Re|Fwd):\s*", "", subject, flags=re.IGNORECASE)
    print(f"Cleaned Subject: {clean_subject}")  # Debugging line to see the cleaned subject
    
    # Updated to match the conversation key directly in the subject
    match = re.search(r'(\w{16})', clean_subject)  # Looking for a 16-character alphanumeric key
    if match:
        print(f"Conversation Key Found: {match.group(1)}")  # Debugging line to see the extracted key
    else:
        print("No conversation key found.")  # Debugging line if no key is found
    return match.group(1) if match else None


def encryptor(emails):
    import hashlib
    email_hashes = []
    
    for email in emails:
        hash_object = hashlib.sha256()
        email_data = f"{email['date']}{email['from']}{email['to']}{email['subject']}{email['body']}"
        hash_object.update(email_data.encode('utf-8'))
        email_hashes.append(hash_object.hexdigest())
    
    return email_hashes

def log_error(message):
    print(message)
    
def log_success(message):
    message = message #if we comment the "print" line, the function still doing something, what is mandatory
    print(message)
    
