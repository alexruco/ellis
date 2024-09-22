# get_env.py

import os
from dotenv import load_dotenv

# Optionally clear existing environment variables
def clear_env_vars(*args):
    for var in args:
        os.environ.pop(var, None)

# Clear specified environment variables before loading new values
clear_env_vars("EMAIL_USERNAME", "EMAIL_PASSWORD", "IMAP_SERVER")

# Load environment variables from a .env file (optional)
load_dotenv()

# Fetch the credentials and IMAP server from environment variables
USERNAME = os.getenv("EMAIL_USERNAME")
PASSWORD = os.getenv("EMAIL_PASSWORD")
IMAP_SERVER = os.getenv("IMAP_SERVER")

# Optionally set new values manually (you can omit this if you're using a .env file)
os.environ["EMAIL_USERNAME"] = "your_username_here"
os.environ["EMAIL_PASSWORD"] = "your_password_here"
os.environ["IMAP_SERVER"] = "imap.yourserver.com"

# You can include defaults or raise errors if any variable is missing
if not USERNAME or not PASSWORD or not IMAP_SERVER:
    raise EnvironmentError("Please ensure EMAIL_USERNAME, EMAIL_PASSWORD, and IMAP_SERVER are set in your environment.")