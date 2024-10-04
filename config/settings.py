from dotenv import load_dotenv
import os
import ast
import logging

# Configuration du logger global
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def strtobool(val):
    return bool(ast.literal_eval(val.capitalize()))

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Convertir la variable d'environnement DEV_MODE en booléen
DEV_MODE = bool(strtobool(os.getenv('DEV_MODE', 'True')))
if DEV_MODE:
    print(f"Mode développement activé.")
API_KEY = os.getenv('API_KEY')
# Print error if API key is missing else print API key but mask it as a secret
if not API_KEY:
    raise ValueError("API_KEY is not set in environment variables.")

#Parametres database
POSTGRES_DB=os.getenv('POSTGRES_DB')
POSTGRES_USER=os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST=os.getenv('POSTGRES_HOST')
POSTGRES_PORT=os.getenv('POSTGRES_PORT','5432')

# Paramètres modifiables par environnement
PROJECT_ID = os.getenv('PROJECT_ID', 'smshttp-436212')
SUBSCRIPTION_ID = os.getenv('SUBSCRIPTION_ID', 'NewRdvTopic-sub')
SMS_API_URL = os.getenv('SMS_API_URL', 'https://api.httpsms.com/v1/messages/send')
FROM_NUMBER = os.getenv('FROM_NUMBER')
SCHEDULER_INTERVAL_MINUTES = int(os.getenv('SCHEDULER_INTERVAL_MINUTES', 60))
print(f"Interval du scheduler: {SCHEDULER_INTERVAL_MINUTES} minutes.")

# Détection de l'environnement Kubernetes vs local
if os.path.exists('/secrets/service-account.json'):
    CREDENTIALS_PATH = '/secrets/service-account.json'
else:
    CREDENTIALS_PATH = os.getenv('CREDENTIALS_PATH', 'secrets/service-account.json')