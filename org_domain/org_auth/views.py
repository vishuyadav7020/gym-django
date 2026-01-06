import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from authentication.mongo import orgs_collections
from authentication.security import hash_password, check_password
from authentication.utils import send_otp_orgdomain
from authentication.schemas import OrgSchema
from datetime import datetime, timedelta
from django.core.mail import send_mail
from bson import ObjectId
from home.urls import *

# Create your views here.


class OrgLoginRegisterLogout:

    ### ---------------------------------- Login org ---------------------------------- ###

    @staticmethod
    def Orglogin(request):
        if request.method == "POST":
            orgname = request.POST["orgname"].lower()
            password = request.POST["password"]

            org = orgs_collections.find_one({"orgname": orgname})

            if not org or not check_password(password, org["password"]):
                messages.error(request, "Invalid Credentials")
                return redirect("org_login")

            request.session["org_id"] = str(org["_id"])
            request.session["orgname"] = org["orgname"]
            request.session["org_photo"] = org["org_photo"]

            messages.success(request, "Login Successful")
            org_name = request.session.get("orgname")
            return redirect("orghome")

        return render(request, "org_auth/login.html")

    ### ---------------------------------- Register New org ---------------------------------- ###
    @staticmethod
    def Orgregister(request):
        if request.method == "POST":

            orgname = request.POST["orgname"].lower()
            password = request.POST["password"]

            photo = request.FILES.get("photo")
            photo_url = None
            
            if photo:
                org_folder = os.path.join(settings.MEDIA_ROOT, "orgs")
                os.makedirs(org_folder, exist_ok=True)

                file_path = os.path.join(org_folder, photo.name)

                with open(file_path, "wb+") as f:
                    for chunk in photo.chunks():
                        f.write(chunk)
                        
                photo_url = f"/media/orgs/{photo.name}"

            org_data = OrgSchema.create_org(
                owner_first_name=request.POST["ownerfirstname"],
                owner_last_name=request.POST["ownerlastname"],
                orgname=request.POST["orgname"].lower(),
                email=request.POST["email"],
                password=hash_password(password),
                org_photo= photo_url,
            )

            if orgs_collections.find_one({"orgname": orgname}):
                messages.error(request, "orgname Already Exists")
                return redirect("org_register")

            orgs_collections.insert_one(org_data)
            messages.success(request, "Signup Successful")
            return redirect("org_login")
        
        return render(request, "org_auth/register.html")

    ### ---------------------------------- Logout org ---------------------------------- ###
    
    @staticmethod
    def Orglogout(request):
        if not request.session.get("org_id") and not request.session.get("orgname"):
            return redirect('domain')
        
        request.session.flush()
        messages.success(request, "Logged out successfully")
        return redirect("domain")


class OrgForgetResetVerifyPassword:

    @staticmethod
    def OrgforgetPassword(request):

        if request.method == "GET" and not request.META.get("HTTP_REFERER"):
            return redirect('org_login')

        if request.method == "POST":
            orgname = request.POST["orgname"].lower()

            org = orgs_collections.find_one({"orgname": orgname})

            if not org:
                messages.error(request, "orgname does not exist")
                return redirect("org_login")

            send_otp_orgdomain(org)

            request.session["reset_org"] = str(org["_id"])
            messages.success(request, "OTP sent to registered email")
            return redirect("org_verify_otp")

        return render(request, "org_auth/forgetpass.html")

    @staticmethod
    def Orgverify_otp(request):

        if not request.session.get("reset_org"):
            return redirect('org_login')

        if request.method == "POST":
            otp_entered = request.POST["otp"]
            org_id = request.session.get("reset_org")

            org = orgs_collections.find_one({"_id": ObjectId(org_id)})

            if not org or org.get("reset_otp") != otp_entered:
                messages.error(request, "Invalid OTP")
                return redirect("org_verify_otp")

            if datetime.utcnow() > org["reset_otp_expiry"]:
                messages.error(request, "OTP Expired")
                return redirect("org_forgetpass")

            request.session["otp_verified"] = True
            request.session.modified = True
            messages.success(request, "OTP verified")
            return redirect("org_reset_password")

        return render(request, "org_auth/verify_otp.html")

    @staticmethod
    def Orgreset_password(request):

        if not request.session.get("reset_org") or not request.session.get("otp_verified"):
            return redirect("org_login")

        if request.method == "POST":
            new_password = request.POST["password"]
            org_id = request.session["reset_org"]

            orgs_collections.update_one(
                {"_id": ObjectId(org_id)},
                {
                    "$set": {
                        "password": hash_password(new_password)
                    },

                    "$unset": {
                        "reset_otp": " ",
                        "reset_otp_expiry": ""
                    }
                }
            )

            request.session.flush()
            messages.success(request, "Password Reset Successfully")
            return redirect("org_login")

        return render(request, "org_auth/reset_password.html")
