import os

def get_env_variable(var_name):
    """
    Fetches the specified environment variable dynamically.
    
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

# Dynamic functions to access environment variables
def get_username():
    return get_env_variable("EMAIL_USERNAME")

def get_password():
    return get_env_variable("EMAIL_PASSWORD")

def get_imap_server():
    return get_env_variable("IMAP_SERVER")
