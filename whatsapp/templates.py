import requests, json
from django.conf import settings


def send_account_creation_template(to_number, name, email):
    url = (f"{settings.ZIXFLOW_API_BASE_URL}/api/v1/campaign/whatsapp/send")

    payload = {
        "to": to_number,  
        "phoneId": settings.ZIXFLOW_PHONE_ID,
        "templateName": "account_creation",
        "language": "en_US",
        "variables": {
            "body_1": name,
            "body_2": email
        },
        "source": "API",
        "submissionStatus": True
    }

    headers = {
        "Authorization": f"Bearer {settings.ZIXFLOW_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    return response.json()

