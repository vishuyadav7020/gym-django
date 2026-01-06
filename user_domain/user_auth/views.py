from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from authentication.mongo import users_collections, members_collections, trainers_collections, orgs_collections
from authentication.security import hash_password, check_password
from authentication.utils import generate_otp, send_otp_userdomain_member, send_otp_userdomain_trainer
from authentication.schemas import UserSchema, MemberSchema, TrainerSchema
from bson import ObjectId
from  django.utils import timezone
from home.urls import *

# Create your views here.
class userLoginRegisterLogout:

    ### ---------------------------------- Login User ---------------------------------- ###

    @staticmethod
    def userlogin(request):
        if request.method == "POST":
            email = request.POST["email"].lower()
            password = request.POST["password"]
            category = request.POST["category"]

            if category == "trainer":
                trainer = trainers_collections.find_one({"trainer_email" : email})
                if not trainer or not check_password(password, trainer["trainer_password"]):
                    messages.error(request, "Inavalid Credentials")
                    return redirect("user_login")
                
                request.session["org_id"] = str(trainer["org_id"])
                request.session["trainer_id"] = str(trainer["_id"])
                request.session["trainer_name"] = trainer["trainer_name"]
                #request.session["category"] = category

                print(request.session["org_id"])
                print(request.session["trainer_id"])
                print(request.session["trainer_name"])
                #print(request.session["category"])

                messages.success(request, "Login Successfully")
                return redirect("user_trainer_home")
            
            if category == "member":
                return redirect("undermaintance")

        return render(request, "user_auth/login.html")

    ### ---------------------------------- Register New User ---------------------------------- ###
    @staticmethod
    def userregister(request):
        if request.method == "POST":
            
            # username = request.POST["email"].lower()
            # password = request.POST["password"]
            
            # user_data = UserSchema.create_user(
            #     first_name = request.POST["firstname"],
            #     last_name = request.POST["lastname"],
            #     username = request.POST["username"].lower(),
            #     orgname = request.POST["orgname"].lower(),
            #     email = request.POST["email"],
            #     password = hash_password(password)
            # )

            # if users_collections.find_one({"username": username}):
            #     messages.error(request, "username already exists")
            #     return redirect("user_register")

            # users_collections.insert_one(user_data)

            # messages.success(request, "Signup Successful")
            return redirect("undermaintance")
        return render(request, "user_auth/register.html")

    ### ---------------------------------- Logout User ---------------------------------- ###
    @staticmethod
    def userlogout(request):
        request.session.flush()
        messages.success(request, "Logged out successfully")
        return redirect("user_login")



######################### ---------------------------------------------------------------------------------------------------------------------------


class userForgetResetVerifyPassword:

    @staticmethod
    def userforgetPassword(request):
        
        if request.method=="GET" and not request.META.get("HTTP_REFERER"):
            return redirect('user_login')
        
        list_orgnames = list(orgs_collections.find())
        for list_orgname in list_orgnames:
            list_orgname["id"] = str(list_orgname["_id"])

        if request.method == "POST":

            if request.POST["category"] == "trainer":
                email = request.POST["email"].lower()
                org_id = request.POST["gymname"].lower()

                org = orgs_collections.find_one({"_id" : ObjectId(org_id)})
                trainer = trainers_collections.find_one({
                    "org_id" : org_id,
                    "trainer_email" : email
                })

                # print(email)
                # print(org["orgname"])
                # print(org_id)
                # print(trainer)

                if not trainer:
                    messages.error(request, f"Trainer does not exist with {org["orgname"].upper()}")
                    messages.error(request, f"Contact The Owner Of {org["orgname"].upper()}")
                    return redirect("user_login")
                
                send_otp_userdomain_trainer(trainer)

                request.session["reset_trainer"] = str(trainer["_id"])
                messages.success(request, "OTP sent to Registered Email")
                print(request.session["reset_trainer"])
                return redirect("user_verify_otp")
            
            if request.POST["category"] == "member":

                email = request.POST["email"].lower()
                org_id = request.POST["gymname"].lower()

                org = orgs_collections.find_one({"_id" : ObjectId(org_id)})
                member = members_collections.find_one({
                    "org_id" : org_id,
                    "email" : email
                })

                if not member:
                    messages.error(request, f"Member does not exist with {org["orgname"].upper()}")
                    return redirect("user_login")
                
                send_otp_userdomain_member(member)

                request.session["reset_member"] = str(member["_id"]) # type: ignore
                messages.success(request, "OTP sent to Registered Email")
                return redirect("user_verify_otp")


            # username = request.POST["username"].lower()

            # user = users_collections.find_one({"username": username})

            # if not user:
            #     messages.error(request, "Username does not exist")
            #     return redirect("user_login")
            
            # send_otp_userdomain(user)

            # request.session["reset_user"] = str(user["_id"])
            # messages.success(request, "OTP sent to registered email")
            # return redirect("user_verify_otp")

        return render(request, "user_auth/forgetpass.html", {"orgnames" : list_orgnames})
    
    @staticmethod
    def userverify_otp(request):
        
        if not request.session.get("reset_trainer") or request.session.get("reset_member"):
            return redirect('user_login')
        
        if request.method == "POST":
            otp_entered = request.POST["otp"]

            if request.session.get("reset_member"):
                member_id = request.session("reset_member")

                member = members_collections.find_one({"_id" : ObjectId(member_id)})


                if not member or member.get("reset_otp") != otp_entered:
                    messages.error(request, "Invalid OTP")
                    return redirect("user_verify_otp")
                
                expiry = member["reset_otp_expiry"]

                if timezone.is_naive(expiry):
                    expiry = timezone.make_aware(expiry, timezone.get_current_timezone())

                if timezone.now() > expiry:
                    messages.error(request, "OTP Expired")
                    return redirect("user_forgetpass")
                
                request.session["otp_verified"] = True
                request.session.modified = True
                messages.success(request, "OTP verified")
                print("VERIFY OTP SESSION:", dict(request.session))
                return redirect("user_reset_password")
            
            if request.session.get("reset_trainer"):

                trainer_id = request.session["reset_trainer"]

                trainer = trainers_collections.find_one({"_id" : ObjectId(trainer_id)})

                if not trainer or trainer.get("reset_otp") != otp_entered:
                    messages.error(request, "Invalid OTP")
                    return redirect("user_verify_otp")
                
                expiry = trainer["reset_otp_expiry"]
                if timezone.is_naive(expiry):
                    expiry = timezone.make_aware(expiry, timezone.get_current_timezone())

                if timezone.now() > expiry:     
                    messages.error(request, "OTP Expired")
                    return redirect("user_forgetpass")
                
                request.session["otp_verified"] = True
                messages.success(request, "OTP Verified")
                print("VERIFY OTP SESSION:", dict(request.session))
                return redirect("user_reset_password")

            # member_id = request.session.get("reset_member")
            # trainer_id = request.session.get("reset_trainer")
            
            # member = members_collections.find_one({"_id" : ObjectId(member_id)})
            # trainer = trainers_collections.fing_one({})
            # user = users_collections.find_one({"_id" : ObjectId(user_id)})
            
            # if not user or user.get("reset_otp") != otp_entered:
            #     messages.error(request, "Invalid OTP")
            #     return redirect("user_verify_otp")
            
            # if datetime.utcnow() > user["reset_otp_expiry"]:
            #     messages.error(request, "OTP Expired")
            #     return redirect ("user_forgetpass")
            
            # request.session["otp_verified"] = True
            # request.session.modified = True
            # messages.success(request, "OTP verified")
            # print("VERIFY OTP SESSION:", dict(request.session))
            # return redirect("user_reset_password")
        
        return render(request, "user_auth/verify_otp.html")
    
    
    @staticmethod
    def userreset_password(request):
        
        
        if not ( request.session.get("reset_member") or request.session.get("reset_trainer")) or not request.session.get("otp_verified"):
            return redirect("user_login")
        
        if request.method == "POST":
            new_password = request.POST["password"]

            if request.session.get("reset_member"):
                
                member_id = request.session["reset_member"]

                members_collections.update_one(
                    {"_id" : ObjectId(member_id)},
                    {
                        '$set' : {
                            "member_password" : hash_password(new_password)
                        },

                        '$unset' : {
                            "reset_otp" : " ",
                            "reset_otp_expiry" : " "
                        }
                    })
                
                request.session.flush()
                messages.success(request, "Password Reset Successfully")
                return redirect("user_login")
            
            if request.session.get("reset_trainer"):
                
                trainer_id = request.session["reset_trainer"]

                trainer = trainers_collections.update_one(
                    {"_id" : ObjectId(trainer_id)},
                    {
                        '$set' : {
                            'trainer_password' : hash_password(new_password)
                        },

                        '$unset' : {
                            "reset_otp" : " ",
                            "reset_otp_expiry" : " "
                        }   
                    }
                )

                request.session.flush()
                messages.success(request, "Password Reset Successfully")
                return redirect("user_login")
            # user_id = request.session["reset_user"]
            
            # users_collections.update_one(
            #     {"_id" : ObjectId(user_id)},
            #     {
            #         "$set" : {
            #             "password" : hash_password(new_password)
            #         },
                    
            #         "$unset" : {
            #             "reset_otp" : " ",
            #             "reset_otp_expiry" : ""
            #         }
            #     }
            # )            
            
            
            # request.session.flush()
            # messages.success(request, "Password Reset Successfully")
            # return redirect("user_login")
        
        return render(request, "user_auth/reset_password.html")



