from django.urls import path
from .views import *


urlpatterns = [
    path('login/', OrgLoginRegisterLogout.Orglogin, name='org_login'),
    path('register/', OrgLoginRegisterLogout.Orgregister, name='org_register'),
    path('logout/', OrgLoginRegisterLogout.Orglogout, name='org_logout'),

    path('forgetpass/', OrgForgetResetVerifyPassword.OrgforgetPassword, name='org_forgetpass'),
    path('verifyotp/', OrgForgetResetVerifyPassword.Orgverify_otp, name='org_verify_otp'),
    path('resetpass/', OrgForgetResetVerifyPassword.Orgreset_password, name='org_reset_password'),

]
