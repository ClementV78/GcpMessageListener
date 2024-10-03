def handle_rdv_event(cursor, client_id, rdv_id, rdv_datetime, event_type, event_datetime):
    print(f"Traitement de l'événement {event_type} pour le rendez-vous {rdv_id}...")

    # Vérifier si le rendez-vous existe déjà
    cursor.execute("""SELECT rdv_id, last_event_type FROM rdv WHERE rdv_id = ?""", (rdv_id,))
    rdv = cursor.fetchone()

    if rdv:
        rdv_id = rdv[0]
        last_event_type = rdv[1]
        print(f"last_event_type: {last_event_type}, new_event_type: {event_type}")
        # Si le type d'événement a changé, mettre confirmation_sms à NULL
        if last_event_type != event_type:
            print(f"Changement de type d'événement détecté : {last_event_type} -> {event_type}. Mise à jour de confirmation_sms à NULL.")           
            # Construction manuelle de la requête pour affichage uniquement (pas pour exécution)
            sql_query = """
                UPDATE rdv
                SET rdv_datetime = '{}', last_event_type = '{}', last_event_datetime = '{}', status = '{}', confirmation_sms = NULL
                WHERE rdv_id = '{}';
            """.format(rdv_datetime, event_type, event_datetime, event_type, rdv_id)

            # Afficher la requête pour le débogage
            print("Requête SQL exécutée :", sql_query)

            # Exécution sûre avec des placeholders (évite SQL injection)
            cursor.execute("""
                UPDATE rdv
                SET rdv_datetime = ?, last_event_type = ?, last_event_datetime = ?, status = ?, confirmation_sms = NULL
                WHERE rdv_id = ?
            """, (rdv_datetime, event_type, event_datetime, event_type, rdv_id))
        else:
            # Si le type d'événement n'a pas changé, mise à jour classique sans toucher à confirmation_sms
            cursor.execute("""
                UPDATE rdv
                SET rdv_datetime = ?, last_event_type = ?, last_event_datetime = ?, status = ?
                WHERE rdv_id = ?
            """, (rdv_datetime, event_type, event_datetime, event_type, rdv_id))
        
        print(f"Rendez-vous {rdv_id} mis à jour avec l'événement {event_type}.")
    else:
        # Si le rendez-vous n'existe pas, on le crée
        print(f"Création d'un nouveau rendez-vous {rdv_id} pour le client {client_id}...")
        cursor.execute("""
            INSERT INTO rdv (rdv_id, client_id, rdv_datetime, last_event_type, last_event_datetime, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (rdv_id, client_id, rdv_datetime, event_type, event_datetime, event_type))
        rdv_id = cursor.lastrowid
        print(f"Nouveau rendez-vous {rdv_id} créé.")

    # Ajouter un nouvel événement dans la table rdv_event
    cursor.execute("""
        INSERT INTO rdv_event (rdv_id, event_type, event_datetime)
        VALUES (?, ?, ?)
    """, (rdv_id, event_type, event_datetime))
    print(f"Événement {event_type} ajouté pour le rendez-vous {rdv_id}.")

    return rdv_id
