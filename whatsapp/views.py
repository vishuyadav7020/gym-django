from .templates import send_whatsapp_template
from django.http import JsonResponse

def test_whatsapp(phone, orgname, owner_first_name, email):
    return send_whatsapp_template(
        campaign_name="django gym",
        phone=phone,
        user_name=orgname,
        template_params=[
            orgname,
            owner_first_name,
            email,
        ],
        tags=["org_test", "test_login"],
    )


def send_org_account_created(phone, admin_name, org_name, login_url):
    return send_whatsapp_template(
        campaign_name="org_account_created",
        phone=phone,
        user_name=admin_name,
        template_params=[
            admin_name,
            org_name,
            login_url,
        ],
        tags=["org", "account_created"],
    )


def send_org_password_reset_otp(phone, user_name, otp):
    return send_whatsapp_template(
        campaign_name="org_password_reset_otp",
        phone=phone,
        user_name=user_name,
        template_params=[otp],
        tags=["security", "otp"],
    )

def send_member_added(phone, member_name, org_name, login_url):
    return send_whatsapp_template(
        campaign_name="member_added_success",
        phone=phone,
        user_name=member_name,
        template_params=[
            member_name,
            org_name,
            login_url,
        ],
        tags=["member", "onboarding"],
    )


def send_membership_expiry(
    phone,
    member_name,
    org_name,
    days_left,
    expiry_date,
):
    return send_whatsapp_template(
        campaign_name="membership_expiry_reminder",
        phone=phone,
        user_name=member_name,
        template_params=[
            member_name,
            org_name,
            str(days_left),
            expiry_date,
        ],
        tags=["membership", "expiry"],
    )

def send_membership_action(
    phone,
    member_name,
    days_left,
    payment_url,
):
    return send_whatsapp_template(
        campaign_name="membership_renewal_action",
        phone=phone,
        user_name=member_name,
        template_params=[
            member_name,
            str(days_left),
            payment_url,
        ],
        tags=["payment", "membership"],
    )
