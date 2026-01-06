from django.urls import path
from .views import *


urlpatterns = [
    path('login/', userLoginRegisterLogout.userlogin, name='user_login'),
    path('register/', userLoginRegisterLogout.userregister, name='user_register'), # pyright: ignore[reportUndefinedVariable]
    path('logout/', userLoginRegisterLogout.userlogout, name='user_logout'),

    path('forgetpass/', userForgetResetVerifyPassword.userforgetPassword, name='user_forgetpass'),
    path('verifyotp/', userForgetResetVerifyPassword.userverify_otp, name='user_verify_otp'), # pyright: ignore[reportUndefinedVariable]
    path('resetpass/', userForgetResetVerifyPassword.userreset_password, name='user_reset_password'),

]
