from django.urls import path
from .views import *

urlpatterns = [
    path("send/", send_whatsapp_message),
    path("webhook/whatsapp/incoming/", whatsapp_incoming_webhook),
    path("test-whatsapp/", test_whatsapp),
]
