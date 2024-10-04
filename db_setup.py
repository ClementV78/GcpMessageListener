def create_tables(cursor):

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        client_id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT,
        phone TEXT NOT NULL UNIQUE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rdv (
        rdv_id TEXT NOT NULL PRIMARY KEY,           
        client_id INTEGER NOT NULL,
        rdv_datetime TEXT NOT NULL,
        last_event_type TEXT NOT NULL,  
        last_event_datetime TEXT NOT NULL,
        confirmation_sms TEXT DEFAULT NULL,
        status TEXT DEFAULT 'en attente',
        FOREIGN KEY (client_id) REFERENCES clients(client_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rdv_event (
        event_id SERIAL PRIMARY KEY,
        rdv_id TEXT NOT NULL,
        event_type TEXT NOT NULL,
        event_datetime TEXT NOT NULL,
        FOREIGN KEY (rdv_id) REFERENCES rdv(rdv_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS relance_sms (
        relance_id SERIAL PRIMARY KEY,
        rdv_id TEXT NOT NULL,
        send_datetime TEXT NOT NULL,
        response TEXT,
        type TEXT NOT NULL,  
        FOREIGN KEY (rdv_id) REFERENCES rdv(rdv_id)
    );
    """)

    print("Tables créées ou déjà existantes.")
