from django.urls import path
from .views import *

urlpatterns = [
    path("home/", user_member_home, name="user_member_home"),
]
