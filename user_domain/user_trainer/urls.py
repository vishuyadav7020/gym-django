from django.urls import path
from .views import *
urlpatterns = [
    path("home/", user_trainer_home, name="user_trainer_home"),
]
