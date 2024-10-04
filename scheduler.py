from apscheduler.schedulers.background import BackgroundScheduler
from db_manager import connect_db, insert_relance_sms
from sms_handler import send_sms
from datetime import datetime, timedelta
from babel.dates import format_datetime
import pytz
from config.settings import SCHEDULER_INTERVAL_MINUTES

paris_tz = pytz.timezone("Europe/Paris")

def check_and_send_confirmation():
    print("Vérification des rendez-vous pour envoi de SMS de confirmation...")
    conn = connect_db()
    cursor = conn.cursor()

    now = datetime.now(pytz.utc)
    limit_time = now + timedelta(hours=48)

    cursor.execute("""
        SELECT rdv.rdv_id, rdv.rdv_datetime, clients.name, clients.phone
        FROM rdv
        JOIN clients ON rdv.client_id = clients.client_id
        WHERE rdv.confirmation_sms IS NULL
        AND rdv.rdv_datetime > ?
        AND rdv.rdv_datetime < ?
    """, (now.isoformat(), limit_time.isoformat()))

    rows = cursor.fetchall()

    for row in rows:
        rdv_id = row[0]
        rdv_datetime = row[1]
        name = row[2]
        phone = row[3]

        rdv_dt = datetime.fromisoformat(rdv_datetime).astimezone(paris_tz)
        formatted_rdv_datetime = format_datetime(rdv_dt, "EEEE d MMMM y 'à' HH'h'mm", locale='fr_FR')

        send_sms(phone, name, formatted_rdv_datetime)
        print(f"SMS de confirmation envoyé pour le rendez-vous {rdv_id}.")

        cursor.execute("""
            UPDATE rdv
            SET confirmation_sms = 'sent'
            WHERE rdv_id = ?
        """, (rdv_id,))
        print(f"Champ 'confirmation_sms' mis à jour pour le rendez-vous {rdv_id}.")

        insert_relance_sms(cursor, rdv_id, datetime.now().isoformat(), "première relance")
        print(f"Relance SMS insérée pour le rendez-vous {rdv_id}.")

    conn.commit()
    conn.close()

    print(f"SMS de confirmation envoyés pour {len(rows)} rendez-vous.")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_and_send_confirmation, 'interval', minutes=SCHEDULER_INTERVAL_MINUTES)
    scheduler.start()
    print("Scheduler APScheduler démarré pour l'envoi des SMS toutes les heures.")
