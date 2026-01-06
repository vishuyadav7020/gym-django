from bson import ObjectId
import random
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from .mongo import users_collections, orgs_collections, trainers_collections, members_collections
import secrets, string



def generate_otp():
    return str(random.randint(100000, 999999))

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

def send_otp_userdomain_member(member):
    
    otp = generate_otp()
    expiry = timezone.now() + timedelta(minutes=10)
    
    org = orgs_collections.find_one({"_id" : ObjectId(member["org_id"])})
    members_collections.update_one(
        {"_id": member["_id"]},
        {"$set": {
            "reset_otp": otp,
            "reset_otp_expiry": expiry
            }}
    )
    send_mail(
                f"Hello {member["first_name"].upper()} {member["last_name"].upper()}\n",            
                f"Password Reset Code for your {org["orgname"].upper()} Member Account is : {otp}\n",
                "noreply@project_1.com",
                [member["email"]],
                fail_silently=False,
            )    
    
def send_otp_userdomain_trainer(trainer):
    
    otp = generate_otp()
    expiry = timezone.now() + timedelta(minutes=10)
    
    org = orgs_collections.find_one({"_id" : ObjectId(trainer["org_id"])})
    trainers_collections.update_one(
        {"_id": trainer["_id"]},
        {"$set": {
            "reset_otp": otp,
            "reset_otp_expiry": expiry
            }}
    )
    send_mail(
                f"Hello {trainer["trainer_name"].upper()}\n",            
                f"Password Reset Code for your {org["orgname"].upper()} Trainer Account is : {otp}\n",
                "noreply@project_1.com",
                [trainer["trainer_email"]],
                fail_silently=False,
            )   
    
def send_otp_orgdomain(org):
    
    otp = generate_otp()
    expiry = timezone.now() + timedelta(minutes=10)
    
    orgs_collections.update_one(
        {"_id": org["_id"]},
        {"$set": {
            "reset_otp": otp,
            "reset_otp_expiry": expiry
            }}
    )
    send_mail(
                f"Password Reset Code for {org["orgname"].upper()} ",
                f"Your password reset code is: {otp}",
                "noreply@project_1.com",
                [org["email"]],
                fail_silently=False,
            )
    
def generate_password_trainer_email(trainer_email, orgname):

    passw = generate_password()

    subject = "Trainer Login Credentials"
    message = (
        f"Your trainer account for {orgname} has been created.\n\n"
        f"user Name:- {trainer_email}\n"
        f"Password:- {passw}\n\n"
        f"Please change your password after first login."
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [trainer_email],
        fail_silently=False,
    )
    
    return passw
