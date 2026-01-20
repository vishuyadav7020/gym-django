import requests
from django.conf import settings


def send_whatsapp_template(
    *,
    campaign_name: str,
    phone: str,
    user_name: str,
    template_params: list,
    tags: list | None = None,
    attributes: dict | None = None,
    media: dict | None = None,
):
    """
    Generic AiSensy WhatsApp sender
    """

    payload = {
        "apiKey": settings.AISENSY_API_KEY,
        "campaignName": campaign_name,
        "destination": phone,              # +9198XXXXXXXX
        "userName": user_name,
        "source": settings.AISENSY_SOURCE,
        "templateParams": template_params,
    }

    if tags:
        payload["tags"] = tags

    if attributes:
        payload["attributes"] = attributes

    if media:
        payload["media"] = media

    response = requests.post(
        settings.AISENSY_API_URL,
        json=payload,
        timeout=15
    )

    try:
        return response.status_code, response.json()
    except Exception:
        return response.status_code, response.text
