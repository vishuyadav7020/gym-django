from django.shortcuts import render

# Create your views here.

def user_member_home(request):
    return render(request, "user_member_home.html")

