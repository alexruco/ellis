# ellis/emails_handler.py
from ellis.utils import extract_email_address, generate_email_hash, is_valid_email
from ellis.conversation_handler import process_email
import os
from ellis.db_connector import get_connection

def normalize_hash(hash_value):
    """Normaliza um hash removendo espaços e aplicando lower-case."""
    return hash_value.strip().lower()

def filter_unprocessed_emails(emails_with_hashes):
    """
    Filtra os emails que já foram processados com base no hash.

    Args:
        emails_with_hashes (list of dict): Lista de emails, cada um contendo uma chave 'hash'.

    Returns:
        list de dict: Lista de emails não processados.
    """
    hashes_to_check = [normalize_hash(email["hash"]) for email in emails_with_hashes]
    print(f"Hashes recém-gerados: {hashes_to_check}")

    if not hashes_to_check:
        return []

    # Conectar ao banco de dados correto e verificar o caminho
    conn = get_connection()
    print(f"Conectado ao banco de dados: {os.path.abspath('instance.db')}")
    c = conn.cursor()

    # Recuperar todos os hashes armazenados no banco de dados
    c.execute("SELECT email_hash FROM processed_emails")
    stored_hashes = [normalize_hash(row[0]) for row in c.fetchall()]

    # Debug: Imprimir detalhes das hashes armazenadas
    print(f"Hashes armazenados no banco (normalizados): {stored_hashes}")
    print(f"Detalhes das hashes armazenadas: {[{'hash': h, 'length': len(h), 'type': type(h)} for h in stored_hashes]}")

    # Debug: Comparar manualmente cada hash para ver porque não há correspondências
    print("Comparando hashes manualmente:")
    for new_hash in hashes_to_check:
        for stored_hash in stored_hashes:
            if new_hash == stored_hash:
                print(f"Match encontrado! {new_hash} == {stored_hash}")
            else:
                print(f"Sem correspondência: {new_hash} != {stored_hash}")

    # Comparação direta das hashes normalizadas
    processed_hashes = [h for h in hashes_to_check if h in stored_hashes]

    # Imprimir os hashes que já foram processados
    print(f"Hashes que já existem no banco: {processed_hashes}")

    # Filtrar os emails cujos hashes não estão na lista de hashes já processados
    unprocessed_emails = [email for email in emails_with_hashes if normalize_hash(email["hash"]) not in processed_hashes]

    # Imprimir os hashes dos emails que serão processados
    print(f"Hashes dos emails que serão processados: {[email['hash'] for email in unprocessed_emails]}")

    conn.close()
    return unprocessed_emails

def handle_incoming_email(email_data):
    """
    Handles an incoming email by processing it and storing it in the database,
    then retrieves the email history of the sender.

    Args:
        email_data (dict): The email data containing sender, recipient, subject, and body.
    """
    sender_full = email_data["email"]["from"]
    recipient_full = email_data["email"]["to"]

    # Extract the actual email addresses
    sender = extract_email_address(sender_full)
    recipient = extract_email_address(recipient_full)

    # Log the sender and recipient to troubleshoot the issue
    #print(f"Processing email from {sender} to {recipient}")

    # Validate the sender and recipient emails
    if is_valid_email(sender) and is_valid_email(recipient):
        # Generate a unique hash for the email
        email_data["hash"] = generate_email_hash(email_data)

        # Process the email (store in DB and mark as processed)
        process_email(email_data)
        print(f"Email from {sender} processed successfully.")

    else:
        print(f"Invalid sender or recipient email address: {sender_full} or {recipient_full}")
