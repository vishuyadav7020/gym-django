from bson import ObjectId
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from authentication.mongo import members_collections, payments_collections
from authentication.schemas import PaymentSchema
from org_domain.payments.utils import activate_member_after_payment


# Create your views here.

####################### --------------- Dashboard of All Payment to the Corresponding Member --------------- #######################

def payment_home(request):
    
    if not request.session.get("org_id") or not request.session.get("orgname"):
        return redirect("domain")
    
    org_id = request.session.get("org_id")
    payments = list(payments_collections.find({"org_id" : org_id}))
    for payment in payments:
        payment["id"] = str(payment["_id"])
    
    return render(request, "payments/payment_home.html", {"payments" : payments})






####################### ------------------------------- Add a New Payement  ------------------------------- #######################

def payment_add(request):
    
    if not request.session.get("org_id") or not request.session.get("orgname"):
        return redirect("domain")
    
    
    org_id = request.session.get("org_id")
    members = list(members_collections.find({"org_id":org_id}))
    for member in members:
        member["id"] = str(member["_id"])
    
    if request.method=="POST":
    
        member_id = request.POST["member_name"]
        member_details  = members_collections.find_one({
            "_id": ObjectId(member_id),
            "org_id" : request.session.get("org_id")})
        
        membership_type = member_details['membership_type']
        
        payment_data = PaymentSchema.create_payment(
            org_id = request.session.get("org_id"),
            member_id = request.POST["member_name"],
            member_name= f"{member_details['first_name']} {member_details['last_name']}",
            amount = request.POST["amount"],
            payment_method = request.POST["payment_method"],
            status = request.POST["status"],
            payment_date= timezone.now()
        )
        
        payments_collections.insert_one(payment_data)
        activate_member_after_payment(member_id, membership_type)   ### Change the status of Member to Which Payment is Added
        messages.success(request, "Payment Added Successfully")    
        return redirect("payment_home")
    
    return render(request, "payments/payment_add.html", {"members" : members})






####################### ------------------------------- Delete a Payment ------------------------------- #######################

def payment_delete(request, payment_id):
    if not request.session.get("org_id") or not request.session.get("orgname"):
        return redirect("domain")
    
    if request.method == "POST":
        payments_collections.delete_one({
            "_id" : ObjectId(payment_id),
            "org_id" : request.session.get("org_id")
        })
         
        messages.success(request, "Payements")
        return redirect("payment_home")
    
    
    return render(request, "payments/payment_home.html")
