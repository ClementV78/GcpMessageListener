import logging
from db_manager import get_rdv_by_id, update_rdv_with_confirmation_null, update_rdv, insert_rdv, insert_rdv_event
logger = logging.getLogger(__name__)

def handle_rdv_event(cursor, client_id, rdv_id, rdv_datetime, event_type, event_datetime):
    logger.info(f"Traitement de l'événement {event_type} pour le rendez-vous {rdv_id}...")

    rdv = get_rdv_by_id(cursor, rdv_id)
    if rdv:
        rdv_id = rdv[0]
        last_event_type = rdv[1]
        logger.info(f"last_event_type: {last_event_type}, new_event_type: {event_type}")
        
        # Si le type d'événement a changé, mettre confirmation_sms à NULL
        if last_event_type != event_type:
            logger.info(f"Changement de type d'événement détecté : {last_event_type} -> {event_type}. Mise à jour de confirmation_sms à NULL.")
            update_rdv_with_confirmation_null(cursor, rdv_id, rdv_datetime, event_type, event_datetime)
        else:
            # Mise à jour sans changer confirmation_sms
            update_rdv(cursor, rdv_id, rdv_datetime, event_type, event_datetime)
        
        logger.info(f"Rendez-vous {rdv_id} mis à jour avec l'événement {event_type}.")
    else:
        # Si le rendez-vous n'existe pas, on le crée
        logger.info(f"Création d'un nouveau Rendez-vous {rdv_id} pour le client {client_id}...")
        insert_rdv(cursor, rdv_id, client_id, rdv_datetime, event_type, event_datetime)
        logger.info(f"Nouveau rendez-vous {rdv_id} créé.")
    
    # Ajouter un nouvel événement dans la table rdv_event
    insert_rdv_event(cursor, rdv_id, event_type, event_datetime)

    return rdv_id
