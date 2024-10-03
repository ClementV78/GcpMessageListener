from dotenv import load_dotenv
import os
import ast

def strtobool(val):
    return bool(ast.literal_eval(val.capitalize()))

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Convertir la variable d'environnement DEV_MODE en booléen
DEV_MODE = bool(strtobool(os.getenv('DEV_MODE', 'True')))
print(f"Mode développement: {DEV_MODE} (type: {type(DEV_MODE)})")
API_KEY = os.getenv('API_KEY')
# Print error if API key is missing else print API key but mask it as a secret
if not API_KEY:
    raise ValueError("API_KEY is not set in environment variables.")
else:   
    print(f"API_KEY: {'*' * 4}{API_KEY[-4:]}")
    
# Paramètres modifiables par environnement
PROJECT_ID = os.getenv('PROJECT_ID', 'smshttp-436212')
SUBSCRIPTION_ID = os.getenv('SUBSCRIPTION_ID', 'NewRdvTopic-sub')
# Clé API pour envoyer des SMS

SMS_API_URL = "https://api.httpsms.com/v1/messages/send"
FROM_NUMBER = "+33620215946"



# Détection de l'environnement Kubernetes vs local
if os.path.exists('/secrets/service-account.json'):
    CREDENTIALS_PATH = '/secrets/service-account.json'
else:
    CREDENTIALS_PATH = os.getenv('CREDENTIALS_PATH', 'secrets/service-account.json')