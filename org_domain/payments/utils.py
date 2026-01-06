from django.utils import timezone
from bson import ObjectId
from authentication.mongo import members_collections
from org_domain.members.utils import calculate_membership_end

### Change the Status to Active and Change the Membership Start and End Date when Payment to Added of that Member ##
def activate_member_after_payment(member_id, membership_type):
    start = timezone.now()
    end = calculate_membership_end(start, membership_type)

    members_collections.update_one(
        {"_id": ObjectId(member_id)},
        {
            "$set": {
                "status": "active",
                "membership_start": start,
                "membership_end": end
            }
        }
    )
