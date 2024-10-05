# ellis/get_env.py

import os

def get_env_variable(var_name):
    """
    Fetches the specified environment variable.
    
    Args:
        var_name (str): The name of the environment variable.
        
    Returns:
        str: The value of the environment variable.
        
    Raises:
        EnvironmentError: If the variable is not set.
    """
    value = os.getenv(var_name)
    if not value:
        raise EnvironmentError(f"Please ensure {var_name} is set in your environment.")
    return value

# Access environment variables dynamically when needed
USERNAME = get_env_variable("EMAIL_USERNAME")
PASSWORD = get_env_variable("EMAIL_PASSWORD")
IMAP_SERVER = get_env_variable("IMAP_SERVER")

# Optional debugging (remove in production)
print(f"Ellis: Loaded EMAIL_USERNAME: {USERNAME}")
print(f"Ellis: Loaded EMAIL_PASSWORD: {PASSWORD}")
print(f"Ellis: Loaded IMAP_SERVER: {IMAP_SERVER}")
