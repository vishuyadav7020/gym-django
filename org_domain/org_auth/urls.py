from django.urls import path
from .views import *


urlpatterns = [
    path('login/', OrgLoginRegisterLogout.Orglogin, name='org_login'),
    path('register/', OrgLoginRegisterLogout.Orgregister, name='org_register'),
    path('logout/', OrgLoginRegisterLogout.Orglogout, name='org_logout'),

    path('forgetpass/', OrgForgetResetVerifyPassword.OrgforgetPassword, name='org_forgetpass'),
    path('verifyotp/', OrgForgetResetVerifyPassword.Orgverify_otp, name='org_verify_otp'),
    path('resetpass/', OrgForgetResetVerifyPassword.Orgreset_password, name='org_reset_password'),

    path('profile/', OrgProfile.org_profile, name='org_profile'),

    path('account-settings/', OrgAccountSettings.account_settings, name='org_account_settings'),
    path('account-settings/change-photo/', OrgAccountSettings.change_profile_photo, name='org_change_photo'),
    path('account-settings/change-email/', OrgAccountSettings.change_email, name='org_change_email'),
    path('account-settings/change-password/', OrgAccountSettings.change_password, name='org_change_password'),
    path('account-settings/delete/', OrgAccountSettings.delete_account, name='org_delete_account'),

]
