import os
import uuid
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from authentication.mongo import orgs_collections, members_collections, trainers_collections, payments_collections
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


class OrgProfile:

    @staticmethod
    def org_profile(request):
        """Display organization profile with statistics"""
        if not request.session.get("org_id") or not request.session.get("orgname"):
            return redirect("domain")
        
        org_id = request.session.get("org_id")
        
        # Get organization details
        org = orgs_collections.find_one({"_id": ObjectId(org_id)})
        
        if not org:
            messages.error(request, "Organization not found")
            return redirect("orghome")
        
        # Calculate statistics
        total_members = members_collections.count_documents({"org_id": org_id})
        total_trainers = trainers_collections.count_documents({"org_id": org_id})
        total_payments = payments_collections.count_documents({"org_id": org_id})
        
        # Calculate active members (members with active status)
        active_members = members_collections.count_documents({
            "org_id": org_id,
            "status": "active"
        })
        
        # Get recent activity dates
        org_data = {
            "orgname": org.get("orgname", ""),
            "email": org.get("email", ""),
            "owner_first_name": org.get("owner_first_name", ""),
            "owner_last_name": org.get("owner_last_name", ""),
            "org_photo": org.get("org_photo"),
            "created_on": org.get("created_on"),
            "updated_on": org.get("updated_on"),
            "is_active": org.get("is_active", True),
            "total_members": total_members,
            "active_members": active_members,
            "total_trainers": total_trainers,
            "total_payments": total_payments,
        }
        
        return render(request, "org_auth/profile.html", {"org": org_data})

    @staticmethod
    def org_delete_account(request):
        """Delete organization account and all associated data"""
        if not request.session.get("org_id") or not request.session.get("orgname"):
            return redirect("domain")
        
        if request.method == "POST":
            confirm_text = request.POST.get("confirm_text", "").strip().lower()
            orgname = request.session.get("orgname", "").lower()
            
            # Verify confirmation
            if confirm_text != orgname:
                messages.error(request, f"Confirmation failed. Please enter '{orgname}' exactly to confirm deletion.")
                return redirect("org_profile")
            
            org_id = request.session.get("org_id")
            
            # Delete all associated data
            try:
                # Delete members
                members_collections.delete_many({"org_id": org_id})
                
                # Delete trainers
                trainers_collections.delete_many({"org_id": org_id})
                
                # Delete payments
                payments_collections.delete_many({"org_id": org_id})
                
                # Delete organization photo if exists
                org = orgs_collections.find_one({"_id": ObjectId(org_id)})
                if org and org.get("org_photo"):
                    photo_path = os.path.join(settings.MEDIA_ROOT, org["org_photo"].replace("/media/", ""))
                    if os.path.exists(photo_path):
                        os.remove(photo_path)
                
                # Delete organization
                orgs_collections.delete_one({"_id": ObjectId(org_id)})
                
                # Clear session
                request.session.flush()
                
                messages.success(request, "Account deleted successfully. We're sorry to see you go!")
                return redirect("domain")
                
            except Exception as e:
                messages.error(request, f"Error deleting account: {str(e)}")
                return redirect("org_account_settings")
        
        return redirect("org_account_settings")


class OrgAccountSettings:

    @staticmethod
    def account_settings(request):
        """Display account settings page"""
        if not request.session.get("org_id") or not request.session.get("orgname"):
            return redirect("domain")
        
        org_id = request.session.get("org_id")
        org = orgs_collections.find_one({"_id": ObjectId(org_id)})
        
        if not org:
            messages.error(request, "Organization not found")
            return redirect("orghome")
        
        org_data = {
            "orgname": org.get("orgname", ""),
            "email": org.get("email", ""),
            "owner_first_name": org.get("owner_first_name", ""),
            "owner_last_name": org.get("owner_last_name", ""),
            "org_photo": org.get("org_photo"),
        }
        
        return render(request, "org_auth/account_settings.html", {"org": org_data})

    @staticmethod
    def change_profile_photo(request):
        """Update organization profile photo"""
        if not request.session.get("org_id") or not request.session.get("orgname"):
            return redirect("domain")
        
        if request.method == "POST":
            org_id = request.session.get("org_id")
            org = orgs_collections.find_one({"_id": ObjectId(org_id)})
            
            if not org:
                messages.error(request, "Organization not found")
                return redirect("org_account_settings")
            
            photo = request.FILES.get("photo")
            if photo:
                # Delete old photo if exists
                if org.get("org_photo"):
                    old_photo_path = os.path.join(settings.MEDIA_ROOT, org["org_photo"].replace("/media/", ""))
                    if os.path.exists(old_photo_path):
                        os.remove(old_photo_path)
                
                # Save new photo
                org_folder = os.path.join(settings.MEDIA_ROOT, "orgs")
                os.makedirs(org_folder, exist_ok=True)
                
                # Generate unique filename
                file_extension = os.path.splitext(photo.name)[1]
                unique_filename = f"{uuid.uuid4()}{file_extension}"
                file_path = os.path.join(org_folder, unique_filename)
                
                with open(file_path, "wb+") as f:
                    for chunk in photo.chunks():
                        f.write(chunk)
                
                photo_url = f"/media/orgs/{unique_filename}"
                
                # Update database
                orgs_collections.update_one(
                    {"_id": ObjectId(org_id)},
                    {
                        "$set": {
                            "org_photo": photo_url,
                            "updated_on": datetime.utcnow()
                        }
                    }
                )
                
                # Update session
                request.session["org_photo"] = photo_url
                request.session.modified = True
                
                messages.success(request, "Profile photo updated successfully!")
            else:
                messages.error(request, "Please select a photo to upload")
            
            return redirect("org_account_settings")
        
        return redirect("org_account_settings")

    @staticmethod
    def change_email(request):
        """Change organization email"""
        if not request.session.get("org_id") or not request.session.get("orgname"):
            return redirect("domain")
        
        if request.method == "POST":
            org_id = request.session.get("org_id")
            new_email = request.POST.get("email", "").strip().lower()
            password = request.POST.get("password", "")
            
            if not new_email or not password:
                messages.error(request, "Email and password are required")
                return redirect("org_account_settings")
            
            org = orgs_collections.find_one({"_id": ObjectId(org_id)})
            
            if not org:
                messages.error(request, "Organization not found")
                return redirect("org_account_settings")
            
            # Verify password
            if not check_password(password, org["password"]):
                messages.error(request, "Incorrect password")
                return redirect("org_account_settings")
            
            # Check if email already exists
            existing_org = orgs_collections.find_one({"email": new_email})
            if existing_org and str(existing_org["_id"]) != org_id:
                messages.error(request, "Email already in use by another organization")
                return redirect("org_account_settings")
            
            # Update email
            orgs_collections.update_one(
                {"_id": ObjectId(org_id)},
                {
                    "$set": {
                        "email": new_email,
                        "updated_on": datetime.utcnow()
                    }
                }
            )
            
            messages.success(request, "Email updated successfully!")
            return redirect("org_account_settings")
        
        return redirect("org_account_settings")

    @staticmethod
    def change_password(request):
        """Change organization password"""
        if not request.session.get("org_id") or not request.session.get("orgname"):
            return redirect("domain")
        
        if request.method == "POST":
            org_id = request.session.get("org_id")
            current_password = request.POST.get("current_password", "")
            new_password = request.POST.get("new_password", "")
            confirm_password = request.POST.get("confirm_password", "")
            
            if not current_password or not new_password or not confirm_password:
                messages.error(request, "All password fields are required")
                return redirect("org_account_settings")
            
            if new_password != confirm_password:
                messages.error(request, "New passwords do not match")
                return redirect("org_account_settings")
            
            if len(new_password) < 6:
                messages.error(request, "Password must be at least 6 characters long")
                return redirect("org_account_settings")
            
            org = orgs_collections.find_one({"_id": ObjectId(org_id)})
            
            if not org:
                messages.error(request, "Organization not found")
                return redirect("org_account_settings")
            
            # Verify current password
            if not check_password(current_password, org["password"]):
                messages.error(request, "Current password is incorrect")
                return redirect("org_account_settings")
            
            # Update password
            orgs_collections.update_one(
                {"_id": ObjectId(org_id)},
                {
                    "$set": {
                        "password": hash_password(new_password),
                        "updated_on": datetime.utcnow()
                    }
                }
            )
            
            messages.success(request, "Password changed successfully!")
            return redirect("org_account_settings")
        
        return redirect("org_account_settings")

    @staticmethod
    def delete_account(request):
        """Delete organization account and all associated data"""
        if not request.session.get("org_id") or not request.session.get("orgname"):
            return redirect("domain")
        
        if request.method == "POST":
            confirm_text = request.POST.get("confirm_text", "").strip().lower()
            orgname = request.session.get("orgname", "").lower()
            
            # Verify confirmation
            if confirm_text != orgname:
                messages.error(request, f"Confirmation failed. Please enter '{orgname}' exactly to confirm deletion.")
                return redirect("org_account_settings")
            
            org_id = request.session.get("org_id")
            
            # Delete all associated data
            try:
                # Delete members
                members_collections.delete_many({"org_id": org_id})
                
                # Delete trainers
                trainers_collections.delete_many({"org_id": org_id})
                
                # Delete payments
                payments_collections.delete_many({"org_id": org_id})
                
                # Delete organization photo if exists
                org = orgs_collections.find_one({"_id": ObjectId(org_id)})
                if org and org.get("org_photo"):
                    photo_path = os.path.join(settings.MEDIA_ROOT, org["org_photo"].replace("/media/", ""))
                    if os.path.exists(photo_path):
                        os.remove(photo_path)
                
                # Delete organization
                orgs_collections.delete_one({"_id": ObjectId(org_id)})
                
                # Clear session
                request.session.flush()
                
                messages.success(request, "Account deleted successfully. We're sorry to see you go!")
                return redirect("domain")
                
            except Exception as e:
                messages.error(request, f"Error deleting account: {str(e)}")
                return redirect("org_account_settings")
        
        return redirect("org_account_settings")
