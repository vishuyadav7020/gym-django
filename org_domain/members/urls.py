from django.urls import  path
from .views import *


urlpatterns = [
    path('', member_home, name="member_home"),
    path('add/', member_add, name='member_add'),
    path('delete/<str:member_id>', member_delete, name="member_delete"),
]