from datetime import timedelta
from django.utils import timezone
from authentication.mongo import members_collections, payments_collections


### ---------- Calulate the Ending Date of the Member Based on the Membership Type ---------- ###
def calculate_membership_end(start_date, membership_type):    
    if membership_type == "monthly":
        return start_date + timedelta(days=30)
    if membership_type == "quarterly":
        return start_date + timedelta(days=90)
    if membership_type == "yearly":
        return start_date + timedelta(days=365)
    return None

### ---------- Change the Status of Member Whose Membership ending date is than Now ---------- ###
def auto_expire_members(org_id):
    now = timezone.now()
    members_collections.update_many(
        {
            "org_id": org_id,
            "status": "active",
            "membership_end": {"$lt": now}
        },
        {"$set": {"status": "inactive"}}
    )
