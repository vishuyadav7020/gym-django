from django.shortcuts import render, redirect
from django.contrib import messages
import random
from django.conf import settings

# Create your views here.

# def test_html(request):
#     if request.method == "POST":
#         phone = request.POST.get("phone")
#         message_type = request.POST.get("type")

#         try:
#             if message_type == "otp":
#                 otp = random.randint(100000, 999999)
#                 send_whatsapp_otp(
#                     phone,
#                     otp
#                 )
#                 messages.success(request, f"OTP sent successfully: {otp}")

#             else:
#                 text = request.POST.get("message")
#                 send_whatsapp_message(
#                     phone,
#                     text
#                 )
#                 messages.success(request, "WhatsApp message sent successfully")

#         except Exception as e:
#             messages.error(request, str(e))
#     return render(request, "home/test.html")


class home:

    @staticmethod
    def org_home(request):
        if not request.session.get("orgname") or not request.session.get("org_id"):
            return redirect('org_login')
        return render(request, "home/org_home.html")
    
    @staticmethod
    def user_home(request):
        if not request.session.get("username") or not request.session.get("user_id"):
            return redirect('user_login')
        return render(request, "home/user_home.html")


def domain(request):

    if request.method == "POST":
        domain = request.POST.get("domain")

        if domain not in ["user", "org"]:
            return redirect("domain")

        request.session["login_domain"] = domain
        request.session.modified = True

        if domain == "user":
            return redirect("user_login")
        else:
            return redirect("org_login")
        
    request.session.flush()
    return render(request, "home/select_domain.html")

def underMaintance(request):
    return render(request, "home/undermaintance.html")
