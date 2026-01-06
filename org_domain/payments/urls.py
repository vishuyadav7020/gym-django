from django.urls import path
from .views import *
from home.urls import *

urlpatterns = [
    path('', payment_home, name="payment_home"),
    path('/add/', payment_add, name='payment_add'),
    path('/delete/<str:payment_id>', payment_delete, name="payment_delete")
]
