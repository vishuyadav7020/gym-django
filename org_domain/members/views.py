from  bson import ObjectId
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect
from authentication.mongo import members_collections, payments_collections
from authentication.schemas import MemberSchema
from org_domain.members.utils import auto_expire_members


# Create your views here.

####################### ------------------------ Dashboard of All registered Members ------------------------ #######################

def member_home(request):
    if not request.session.get("org_id") and not request.session.get("orgname"):
        return redirect("domain")
    
    org_id = request.session.get("org_id")
    
    auto_expire_members(org_id) ## If Membership Expires than change the Status to Inactive
    
    members = list( members_collections.find({"org_id": org_id})) 
    for member in members:
        member["id"] = str(member["_id"])

        payment_exist = payments_collections.find_one({
            "org_id" : org_id,
            "member_id" : member["id"]
        })

        member["has_payment"] = True if payment_exist else False
        
    return render(request, "members/member_home.html", {"members" : members})






####################### ------------------------------- Add a New Member ------------------------------- #######################

def member_add(request):
    if not request.session.get("org_id") and not request.session.get("orgname"):
        return redirect("domain")
    
    next_url = request.GET.get("next") or request.session.get("orgname")

    if request.method == "POST":

        first_name = request.POST["first_name"].lower()
        phone = request.POST["phone"]
        
        if members_collections.find_one({"phone": phone}) and members_collections.find_one({"first_name": first_name}):
            messages.error(request, "Memeber Already Exists")
            return redirect("member_add")
        
        member_add_data = MemberSchema.create_member(
            org_id = request.session.get("org_id"),
            first_name = request.POST["first_name"].lower(),
            last_name = request.POST["last_name"].lower(),
            email = request.POST["email"].lower(),
            phone = request.POST["phone"],
            membership_type = request.POST['membership_type'],
            gender = request.POST["gender"].lower(),
            joined_on = timezone.now()
        )
        
        members_collections.insert_one(member_add_data)
        messages.success(request, "Member Added Successfully")
        next_url = request.GET.get("next")
        if(next_url):
            return redirect(next_url)
        return redirect("member_home")

    return render(request, 'members/member_add.html', {"next":next_url})






####################### ------------------------------- Delete a Member ------------------------------- #######################

def member_delete(request, member_id):
    if not request.session.get("org_id") and not request.session.get("orgname"):
        return redirect("domain")
    
    if request.method == "POST":

        delete_payments = request.POST.get("delete_payments")
        org_id = request.session.get("org_id")

        ############# ---------- if Member has a payment, it will ask to delete only the Member or delete both Member and is's payment
        ############# ---------- if Member has no Payment, it will directly delete the Member ---------- ###############

        if delete_payments == "yes":
            payments_collections.delete_many({
                "org_id" : org_id,
                "member_id" : member_id
            })

            members_collections.delete_one({
                "_id": ObjectId(member_id),
                "org_id" : request.session.get("org_id")
            })
            
            messages.success(request, "Member and Payemt Histroy Deleted Successfully")

        else:
            members_collections.delete_one({
                "_id": ObjectId(member_id),
                "org_id" : request.session.get("org_id")
            })
            messages.success(request, "Member Deleted Successfully")

        return redirect("member_home")
    
    return render(request, "members/member_home.html")

def member_update(request, member_id):

    if not request.session.get("org_id") or not request.session.get("orgname"):
        return redirect("domain")
    
    org_id = request.session.get("org_id")
    
    # Fetch member data
    member = members_collections.find_one({
        "_id": ObjectId(member_id),
        "org_id": org_id
    })
    
    if not member:
        messages.error(request, "Member not found")
        return redirect("member_home")
    
    member["id"] = str(member["_id"])

    if request.method == "POST":
        # Update member data
        update_data = {
            "first_name": request.POST["first_name"].lower(),
            "last_name": request.POST["last_name"].lower(),
            "email": request.POST["email"].lower(),
            "phone": request.POST["phone"],
            "membership_type": request.POST["membership_type"],
            "gender": request.POST.get("gender", "").lower(),
            "status": request.POST.get("status", "active")
        }
        
        members_collections.update_one(
            {"_id": ObjectId(member_id), "org_id": org_id},
            {"$set": update_data}
        )
        
        messages.success(request, "Member Updated Successfully")
        return redirect("member_home")

    return render(request, "members/member_update.html", {"member": member})


