# ellis/__init__.py
from ellis.main import get_history, get_new_messages, send_message
from ellis.db_connector import init_db, get_connection
from ellis.utils import extract_email_address
