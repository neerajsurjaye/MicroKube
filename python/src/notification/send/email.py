import smtplib, os
from email.message import EmailMessage
import json
import logging

logging.basicConfig(level=logging.ERROR)

def notification(message):
    try:
        message = json.loads(message)
        mp3_fid = message["mp3_fid"]
        sender_address = os.environ.get("GMAIL_ADDRESS")
        sender_password = os.environ.get("GMAIL_PASSWORD")
        receiver_address = message["username"]

        msg = EmailMessage()
        msg.set_content(f"mp3 fid : {mp3_fid} is now ready")
        msg["Subject"] = "Mp3 Download"
        msg["From"] = sender_address
        msg["To"] = receiver_address

        logging.error(f"Mail send to : {msg}")
    except Exception as err:
        logging.error(err)
        return err