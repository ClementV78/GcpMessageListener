import logging
import threading
import time
from db_setup import create_tables
from pubsub_listener import start_pubsub_listener
from scheduler import start_scheduler
from db_manager import connect_db

logger = logging.getLogger(__name__)
if __name__ == '__main__':
    conn = connect_db()
    cursor = conn.cursor()
    logger.info("Connexion à la base de données SQLite établie.")
    create_tables(cursor)
    logger.info("Tables créées ou déjà existantes.")
    conn.commit()
    conn.close()

    listener_thread = threading.Thread(target=start_pubsub_listener)
    listener_thread.start()

    start_scheduler()

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        pass
