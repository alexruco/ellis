#utils.py

import re

def log_error(message):
    print(message)
    
def log_success(message):
    message = message #if we comment the "print" line, the function still doing something, what is mandatory
    print(message)
    