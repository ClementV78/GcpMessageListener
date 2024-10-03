from datetime import datetime
import threading
import time
import json
import sqlite3
from google.cloud import pubsub_v1
from google.oauth2 import service_account

from config.settings import CREDENTIALS_PATH, PROJECT_ID, SUBSCRIPTION_ID
from db_manager import connect_db, get_or_insert_client
from event_handler import handle_rdv_event
db_lock = threading.Lock() 

def start_pubsub_listener():
    print("Démarrage du listener Pub/Sub...")
    credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
    subscriber = pubsub_v1.SubscriberClient(credentials=credentials)
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
    
    
    def callback(message):
        global db_lock
        conn = None  # Initialiser 'conn' avant le bloc try
        try :
            print(f"Received message: {message.data.decode('utf-8')}")

            try:
                message_data = json.loads(message.data.decode('utf-8'))
            except json.JSONDecodeError:
                print("Erreur: Impossible de décoder le message JSON")
                message.ack()
                return

            name = message_data.get('name')
            email = message_data.get('email')
            phone = message_data.get('phone')
            rdv_datetime = message_data.get('rdv_datetime')
            rdv_id = message_data.get('rdv_id')
            event_type = message_data.get('event_type')
            event_datetime = message_data.get('event_datetime', datetime.now().isoformat())

            if not (name and phone and rdv_datetime and event_type and rdv_id):
                print("Données manquantes dans le message Pub/Sub, enregistrement ignoré.")
                print(f"Nom: {name}, Téléphone: {phone}, Date RDV: {rdv_datetime}, Type événement: {event_type}, ID RDV: {rdv_id}")
                message.ack()
                return
            try:
                # Acquérir le verrou avant de travailler avec la base de données
                with db_lock:
                    with connect_db() as conn:
                        #conn = connect_db()
                        cursor = conn.cursor()
                        print("Connexion à la base de données établie")
                        client_id = get_or_insert_client(cursor, name, email, phone)
                        print(f"Client trouvé/enregistré avec l'ID {client_id}")
                        handle_rdv_event(cursor, client_id, rdv_id, rdv_datetime, event_type, event_datetime)
                        print(f"Événement enregistré pour le rendez-vous {rdv_id}")
                        conn.commit()   
                        print(f"Commit de la transaction {rdv_id}")      
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    print("Erreur: La base de données est verrouillée, réessai dans 1 seconde...")
                    retries += 1
                    time.sleep(1)  # Attendre 1 seconde avant de réessayer
                else:
                    print(f"Erreur: {e}")
                    raise
            finally:
                # Fermer la connexion seulement si elle a été initialisée
                if conn:
                    conn.close()
                    print("Connexion à la base de données fermée.")
            

            message.ack()
        except Exception as e:
            print(f"Erreur lors du traitement du message : {e}")
        finally:
            # Temporiser le traitement des messages pour éviter une surcharge
            time.sleep(5)  # Pause de 1 seconde entre chaque message

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
