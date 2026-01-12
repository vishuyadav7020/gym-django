from twilio.rest import Client
from django.conf import settings
import json

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def send_whatsapp_otp(receiver_phonenumber, otp):
    whatsapp_otp = client.messages.create(
        from_=settings.TWILIO_WHATSAPP_NUMBER,
        to=f"whatsapp:+{receiver_phonenumber}",
        content_sid=settings.TWILIO_OTP_TEMPLATE_SID,
        content_variables=json.dumps({
            "1": str(otp)   # ✅ MUST be string
        })
    )
    return whatsapp_otp.sid

def send_whatsapp_message(receiver_phonenumber, send_whatsapp_message):
    whatsapp_message = client.messages.create(
        from_=settings.TWILIO_WHATSAPP_NUMBER,
        body=send_whatsapp_message,
        to=f'whatsapp:+{receiver_phonenumber}'
    )
    return whatsapp_message.sid
