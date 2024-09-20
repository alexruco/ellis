# create_conversation.py

from db_connector import init_db_pool, get_db_pool

def create_conversation(user_email, system_email, model_email, description, status=True):
    """
    Create a new conversation in the tb_conversation table.
    
    :param user_email: Comma-separated user email addresses.
    :param system_email: Comma-separated system email addresses.
    :param model_email: Comma-separated model email addresses.
    :param description: A brief description of the conversation.
    :param status: Boolean indicating if the conversation is active. Default is True.
    :return: The generated conversation key (conv_key) and the created_at timestamp.
    """
    
    # SQL query to insert a new conversation and return the generated conv_key and created_at
    insert_query = """
        INSERT INTO tb_conversation (user_email, system_email, model_email, description, status)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING conv_key, created_at;
    """
    
    # Initialize database pool if it's not already initialized
    init_db_pool()
    pool = get_db_pool()
    
    if pool is None:
        raise Exception("Failed to initialize the database connection pool.")
    
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            # Execute the insert query and fetch the generated conv_key and created_at
            cur.execute(insert_query, (user_email, system_email, model_email, description, status))
            result = cur.fetchone()
            conv_key, created_at = result
            conn.commit()
            return conv_key, created_at
    finally:
        pool.putconn(conn)

conv_key, created_at = create_conversation(
    user_email="crespo.crespo@gmail.com",
    system_email="alex@ruco.pt",
    model_email="maggie@seomaggie.com",
    description="Discussion about the new project",
    status=True
)

print(f"Conversation created with key: {conv_key} at {created_at}")
