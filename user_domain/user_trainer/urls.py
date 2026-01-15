from django.urls import path
from .views import *

urlpatterns = [
    path("/home/", user_trainer_home, name="user_trainer_home"),
    path("/profile/", user_trainer_profile, name="user_trainer_profile"),
    path("/account-settings/", user_trainer_account_setting, name="user_trainer_account_setting")
]
