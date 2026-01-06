from django.contrib import messages
from django.shortcuts import render, redirect
from authentication.schemas import TrainerSchema
from authentication.mongo import trainers_collections
from authentication.security import hash_password
from authentication.utils import generate_password_trainer_email
from django.utils import timezone

# Create your views here.


def trainer_home(request):
    if not request.session.get("org_id") or not request.session.get("orgname"):
        return redirect("domain")
    
    org_id = request.session.get("org_id")

    trainers = list(trainers_collections.find({"org_id" : org_id}))
    for trainer in trainers:
        trainer["id"] = str(trainer["_id"])

    return render(request, "trainers/trainer_home.html", {"trainers" : trainers})

def trainer_add(request):
    if not request.session.get("org_id") or not request.session.get("orgname"):
        return redirect("domain")
    
    org_id = request.session.get("org_id")
    orgname = request.session.get("orgname")
    if request.method == "POST":
        trainer_name = request.POST["trainer_name"]
        trainer_email = request.POST["trainer_email"].lower()

        if trainers_collections.find_one({"org_id":org_id,"trainer_name" : trainer_name}):
            messages.error(request, "Trainer Already Exist")
            return redirect("trainer_add")
        
        password = hash_password(generate_password_trainer_email(trainer_email, orgname))

        trainer_data = TrainerSchema.create_trainer(
            org_id=org_id,
            trainer_name = request.POST["trainer_name"].lower(),
            trainer_email = request.POST["trainer_email"].lower(),
            trainer_password= password,
            trainer_phone = request.POST["trainer_phone"],  
            trainer_salary = request.POST["trainer_salary"],
            trainer_gender = request.POST["trainer_gender"],
            trainer_join_date = timezone.now()
        )

        trainers_collections.insert_one(trainer_data)
        messages.success(request, "Trainer Added Successfully and Login Credentiali is Send to your Trainer Email")
        return redirect("trainer_home")
    return render(request, "trainers/trainer_add.html")

def trainer_delete(request, trainer_id):
    return render(request, "trainers/trainer_delete.html")


