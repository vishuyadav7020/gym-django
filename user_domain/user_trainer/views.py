from django.shortcuts import render
from authentication.mongo import members_collections, trainers_collections


# Create your views here.

def user_trainer_home(request):
    org_id = request.session["org_id"]
    trainer_id = request.session["trainer_id"]
    trainer_name = request.session["trainer_name"]

    members = list(members_collections.find({
        "org_id" : org_id,
    }))
    for member in members:
        member["id"] = str(member["_id"])

    return render(request, "trainer/user_trainer_home.html", {"members" : members})
