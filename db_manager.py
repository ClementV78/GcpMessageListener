import sqlite3

# Connexion à la base de données
def connect_db(db_path='messages.db'):
    conn = sqlite3.connect(db_path)
    return conn

# Insérer ou obtenir un client par son téléphone
def get_or_insert_client(cursor, name, email, phone):
    cursor.execute("""
        SELECT client_id FROM clients WHERE phone = ?
    """, (phone,))
    result = cursor.fetchone()

    if result:
        print(f"Client {name} {result[0]} trouvé par téléphone.")
        return result[0]  # Le client existe
    else:
        print(f"Client {name} non trouvé par téléphone, insertion en cours...")
        # Insérer le client
        cursor.execute("""
            INSERT INTO clients (name, email, phone)
            VALUES (?, ?, ?)
        """, (name, email, phone))
        print(f"Client {name} inséré avec succès.")
        return cursor.lastrowid  # Retourner l'ID du client inséré

# Insérer un rendez-vous
def insert_rdv(cursor, client_id, rdv_datetime, event_type, event_datetime):
    print(f"Insertion du rendez-vous pour le client {client_id}...")
    cursor.execute("""
        INSERT INTO rdv (client_id, rdv_datetime, event_type, event_datetime)
        VALUES (?, ?, ?, ?)
    """, (client_id, rdv_datetime, event_type, event_datetime))
    print(f"Rendez-vous inséré avec succès. {client_id}")
    return cursor.lastrowid  # Retourne l'ID du rendez-vous inséré

# Mettre à jour un rendez-vous
def update_rdv(cursor, rdv_id, rdv_datetime, event_type, event_datetime):
    print(f"Mise à jour du rendez-vous {rdv_id}...")
    cursor.execute("""
        UPDATE rdv
        SET rdv_datetime = ?, event_type = ?, event_datetime = ?
        WHERE rdv_id = ?
    """, (rdv_datetime, event_type, event_datetime, rdv_id))
    print(f"Rendez-vous mis à jour avec succès. {rdv_id}")

# Insérer une relance SMS
def insert_relance_sms(cursor, rdv_id, send_datetime, type_sms):
    print(f"Insertion d'une relance SMS pour le rendez-vous {rdv_id}...")
    cursor.execute("""
        INSERT INTO relance_sms (rdv_id, send_datetime, type)
        VALUES (?, ?, ?)
    """, (rdv_id, send_datetime, type_sms))
    print(f"Relance SMS insérée avec succès. {rdv_id}")
