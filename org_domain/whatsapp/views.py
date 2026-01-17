import json
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .templates import *


@csrf_exempt
def send_whatsapp_message(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    data = json.loads(request.body)

    payload = {
        "to": data["to"],  # e.g. 918447685442 (NO +)
        "phoneId": settings.ZIXFLOW_PHONE_ID,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": data["message"]
        },
        "source": "API",
        "linkWithRecord": False,
        "submissionStatus": False
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.ZIXFLOW_API_KEY}"
    }

    url = f"{settings.ZIXFLOW_API_BASE_URL}/api/v1/campaign/whatsapp/message/send"

    response = requests.post(url, json=payload, headers=headers)

    return JsonResponse(response.json(), status=response.status_code)


@csrf_exempt   # ✅ THIS IS REQUIRED
def whatsapp_incoming_webhook(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    data = json.loads(request.body)

    print("\n📩 Incoming WhatsApp Webhook:")
    print(json.dumps(data, indent=2))

    sender = data.get("sender", {}).get("number")
    message = data.get("message", {}).get("text", {}).get("body")

    print(f"\n📞 From: {sender}")
    print(f"💬 Message: {message}")

    return JsonResponse({"status": "received"})

@csrf_exempt
def test_whatsapp(request):
    if request.method == "POST":
        result = send_account_creation_template(
            to_number="918447685442",
            name="John",
            email="john@gmail.com"
        )
        return JsonResponse(result)

    return JsonResponse({"error": "Only POST allowed"}, status=405)