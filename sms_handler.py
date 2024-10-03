import json
from config.settings import API_KEY, FROM_NUMBER, DEV_MODE, SMS_API_URL
import uuid

import requests



def send_sms(to, name, rdv_datetime_human):
    print(f"Envoi d'un SMS à {to} pour le rendez-vous le {rdv_datetime_human}")
    content = f"Bonjour {name}, rappel : RDV Sophrologie le {rdv_datetime_human}, merci de confirmer votre présence en répondant 'OUI' à ce sms"
    payload = {
        "content": content,
        "encrypted": False,
        "from": FROM_NUMBER,
        "request_id": str(uuid.uuid4()),
        "to": to
        #"request_id": "unique-request-id"
    }
    headers = {
        "accept": "application/json",
        "x-api-Key": API_KEY,
        "Content-Type": "application/json"
    }
    print(f"DEV_MODE: {DEV_MODE}")
    print(f"Payload SMS: {json.dumps(payload, indent=4)}")
    if DEV_MODE:
        print(f"Mode développement")
    else:
        response = requests.post(SMS_API_URL, headers=headers, data=json.dumps(payload), timeout=60)
        if response.status_code == 200:
            print(f"SMS envoyé à {to}")
        else:
            #ToDo: Update SMS_CONFIRMATION to ERROR in db
            print(f"Échec de l'envoi du SMS à {to}: {response.status_code}, {response.text}")
        return response
