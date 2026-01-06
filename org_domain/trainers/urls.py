from django.urls import path
from .views import *


urlpatterns = [
    path('/home/', trainer_home, name="trainer_home"),
    path('/add/', trainer_add, name="trainer_add"),
    path('/delete/<str:trainer_id>', trainer_delete, name="trainer_delete")
]
