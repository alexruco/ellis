import os
from dotenv import load_dotenv

load_dotenv()  # This loads the environment variables from the .env file

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
IMAP_SERVER = os.getenv('IMAP_SERVER')
DBNAME = os.getenv('DBNAME')
USER = os.getenv('DB_USER')  # Changed to DB_USER to avoid conflict with the USER environment variable in Unix
DB_PASSWORD = os.getenv('DB_PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
