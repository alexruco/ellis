# ellis/get_env.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables and handle missing ones with default values or raise errors
USERNAME = os.getenv('USERNAME')
if not USERNAME:
    raise EnvironmentError("Missing USERNAME in environment variables.")

PASSWORD = os.getenv('PASSWORD')
if not PASSWORD:
    raise EnvironmentError("Missing PASSWORD in environment variables.")

IMAP_SERVER = os.getenv('IMAP_SERVER')
if not IMAP_SERVER:
    raise EnvironmentError("Missing IMAP_SERVER in environment variables.")

DBNAME = os.getenv('DBNAME')
if not DBNAME:
    raise EnvironmentError("Missing DBNAME in environment variables.")

DB_USER = os.getenv('DB_USER')  # DB_USER to avoid conflict with the Unix 'USER'
if not DB_USER:
    raise EnvironmentError("Missing DB_USER in environment variables.")

DB_PASSWORD = os.getenv('DB_PASSWORD')
if not DB_PASSWORD:
    raise EnvironmentError("Missing DB_PASSWORD in environment variables.")

HOST = os.getenv('HOST')
if not HOST:
    raise EnvironmentError("Missing HOST in environment variables.")

PORT = os.getenv('PORT')
try:
    PORT = int(PORT) if PORT else None
    if PORT is None:
        raise EnvironmentError("Missing or invalid PORT in environment variables.")
except ValueError:
    raise ValueError("PORT should be an integer.")
