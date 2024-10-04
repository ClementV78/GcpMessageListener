import psycopg2
import os
from dotenv import load_dotenv
from config.settings import DEV_MODE, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT

# Charger les variables d'environnement si nécessaire
load_dotenv()

# Connexion à la base de données
def connect_db():
    try:
        print(f"Connexion à la base de données PostgreSQL... postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
        conn = psycopg2.connect(
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )
        return conn
    except psycopg2.DatabaseError as e:
        print(f"Erreur de connexion à la base de données : {e}")
        raise

# Récupérer un rendez-vous par son ID
def get_rdv_by_id(cursor, rdv_id):
    cursor.execute("""
        SELECT rdv_id, last_event_type FROM rdv WHERE rdv_id = %s
    """, (rdv_id,))
    return cursor.fetchone()

# Insérer ou obtenir un client par son téléphone
def get_or_insert_client(cursor, name, email, phone):
    try:
        cursor.execute("""
            SELECT client_id FROM clients WHERE phone = %s
        """, (phone,))
        result = cursor.fetchone()

        if result:
            print(f"Client {name} {result[0]} trouvé par téléphone.")
            return result[0]  # Le client existe
        else:
            print(f"Client {name} non trouvé par téléphone, insertion en cours...")
            # Insérer le client avec RETURNING pour obtenir l'ID
            cursor.execute("""
                INSERT INTO clients (name, email, phone)
                VALUES (%s, %s, %s)
                RETURNING client_id
            """, (name, email, phone))
            client_id = cursor.fetchone()[0]
            print(f"Client {name} inséré avec succès. ID : {client_id}")
            return client_id  # Retourner l'ID du client inséré
    except psycopg2.DatabaseError as e:
        print(f"Erreur lors de l'insertion ou la récupération du client : {e}")
        raise

# Insérer un rendez-vous
def insert_rdv(cursor, rdv_id, client_id, rdv_datetime, event_type, event_datetime):
    try:
        print(f"Insertion du rendez-vous pour le client {client_id}...")
        cursor.execute("""
            INSERT INTO rdv (rdv_id, client_id, rdv_datetime, last_event_type, last_event_datetime)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING rdv_id
        """, (rdv_id, client_id, rdv_datetime, event_type, event_datetime))
        rdv_id = cursor.fetchone()[0]
        print(f"Rendez-vous inséré avec succès. ID : {rdv_id}")
        return rdv_id  # Retourner l'ID du rendez-vous inséré
    except psycopg2.DatabaseError as e:
        print(f"Erreur lors de l'insertion du rendez-vous : {e}")
        raise

# Mettre à jour un rendez-vous avec confirmation_sms à NULL
def update_rdv_with_confirmation_null(cursor, rdv_id, rdv_datetime, event_type, event_datetime):
    try:
        cursor.execute("""
            UPDATE rdv
            SET rdv_datetime = %s, last_event_type = %s, last_event_datetime = %s, status = %s, confirmation_sms = NULL
            WHERE rdv_id = %s
        """, (rdv_datetime, event_type, event_datetime, event_type, rdv_id))
        print(f"Rendez-vous {rdv_id} mis à jour avec confirmation_sms à NULL.")
    except psycopg2.DatabaseError as e:
        print(f"Erreur lors de la mise à jour du rendez-vous : {e}")
        raise

# Mettre à jour un rendez-vous sans confirmation_sms
def update_rdv(cursor, rdv_id, rdv_datetime, event_type, event_datetime):
    try:
        print(f"Mise à jour du rendez-vous {rdv_id}...")
        cursor.execute("""
            UPDATE rdv
            SET rdv_datetime = %s, last_event_type = %s, last_event_datetime = %s, status = %s
            WHERE rdv_id = %s
        """, (rdv_datetime, event_type, event_datetime, event_type, rdv_id))
        print(f"Rendez-vous mis à jour avec succès. ID : {rdv_id}")
    except psycopg2.DatabaseError as e:
        print(f"Erreur lors de la mise à jour du rendez-vous : {e}")
        raise

# Insertion d'un nouvel événement pour un rendez-vous
def insert_rdv_event(cursor, rdv_id, event_type, event_datetime):
    try:
        cursor.execute("""
            INSERT INTO rdv_event (rdv_id, event_type, event_datetime)
            VALUES (%s, %s, %s)
        """, (rdv_id, event_type, event_datetime))
        print(f"Événement {event_type} ajouté pour le rendez-vous {rdv_id}.")
    except psycopg2.DatabaseError as e:
        print(f"Erreur lors de l'insertion de l'événement : {e}")
        raise

# Insérer une relance SMS
def insert_relance_sms(cursor, rdv_id, send_datetime, type_sms):
    try:
        print(f"Insertion d'une relance SMS pour le rendez-vous {rdv_id}...")
        cursor.execute("""
            INSERT INTO relance_sms (rdv_id, send_datetime, type)
            VALUES (%s, %s, %s)
        """, (rdv_id, send_datetime, type_sms))
        print(f"Relance SMS insérée avec succès pour le rendez-vous {rdv_id}")
    except psycopg2.DatabaseError as e:
        print(f"Erreur lors de l'insertion de la relance SMS : {e}")
        raise
