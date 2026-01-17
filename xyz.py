import requests

url = "http://localhost:8000/api/v1/campaign/whatsapp/message/send"
#http://127.0.0.1:8000/api/v1/campaign/whatsapp/message/send

payload = {
    "to": "+918447685442",
    "phoneId": "941934725674026",
    "type": "text",
    "text": {
        "preview_url": True,
        "body": "hello"
    },
    "source": "API",
    "linkWithRecord": False,
    "reportURL": "<string>",
    "submissionStatus": False
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)

print(response.text)