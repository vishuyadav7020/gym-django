from django.urls import path
from user_domain.user_auth.urls import *
from org_domain.members import *
from org_domain.payments import *
from org_domain.trainers import *
from .views import *


urlpatterns = [

    path('', domain, name='domain'),
    path('user/home', home.user_home, name='userhome'),
    path('org/home', home.org_home, name='orghome'),
    ##path('test/', test_html, name='test'),
    path('undermaintance/', underMaintance, name="undermaintance")
]
