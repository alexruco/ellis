from josephroulin import send_email
from config import USERNAME, PASSWORD, SMTP_SERVER

def send_message(body, recipient):
    subject = 'Test Email'
    sender_email = 'maggie@seomaggie.com'
    send_email(SMTP_SERVER, 587, USERNAME, PASSWORD, subject, body, recipient, sender_email)
