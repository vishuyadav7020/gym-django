import datetime
from django.utils import timezone
from typing import Dict

class BaseSchema:
    @staticmethod
    def timestamps() -> Dict:
        return{
            "created_on": timezone.now(),
            "updated_on": timezone.now()
        }
        
class UserSchema(BaseSchema):

    @staticmethod
    def create_user(
        *,
        first_name: str,
        last_name: str,
        username: str,
        orgname : str,
        email: str,
        password: bytes,
        organization_id=None
    ) -> Dict:

        return {
            "first_name": first_name,
            "last_name": last_name,
            "username": username.lower(),
            "email": email.lower(),
            "password": password,
            "is_active_member" : True,
            "gym_joined": orgname,
            "organization_id": None,   # None for independent users
            "role": "user",
            "is_active": True,
            **BaseSchema.timestamps()
        }


class OrgSchema(BaseSchema):

    @staticmethod
    def create_org(
        *,
        org_photo : str | None = None,
        owner_first_name: str,
        owner_last_name: str,
        orgname: str,
        email: str,
        password: bytes
        
    ) -> Dict:

        return {
            "orgname": orgname,
            "email": email.lower(),
            "owner_first_name": owner_first_name,
            "owner_last_name": owner_last_name,
            "password": password,
            "org_photo" : org_photo,
            "is_active": True,
            "role": "org_admin",
            **BaseSchema.timestamps()
        }
        
        
class MemberSchema(BaseSchema):

    @staticmethod
    def create_member(
        *,
        org_id,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        gender: str,
        membership_type : str,
        joined_on,
    ) -> Dict:

        return {
            "org_id": org_id,                 # 🔗 Connects to Org
            "first_name": first_name,
            "last_name": last_name,
            "email": email.lower(),
            "phone": phone,
            "gender": gender,
            "membership_type" : membership_type,
            "dob": None,
            "joined_on": joined_on,
            "status": "inactive",
            "membership_start": None,
            "membership_end" : None,
            **BaseSchema.timestamps()
        }


class TrainerSchema(BaseSchema):

    @staticmethod
    def create_trainer(
        *,
        org_id,
        trainer_name: str,
        trainer_email: str,
        trainer_password: bytes,
        trainer_phone: str,
        trainer_salary: float,
        trainer_gender : str,
        trainer_join_date : timezone.now(), # pyright: ignore[reportInvalidTypeForm]
        status: str = "active"
    ) -> Dict:

        return {
            "org_id": org_id,                 # 🔗
            "trainer_name": trainer_name,
            "trainer_email": trainer_email.lower(),
            "trainer_phone": trainer_phone,
            "specialization": None,
            "experience_years": None,
            "trainer_gender" : trainer_gender,
            "trainer_salary": trainer_salary,
            "trainer_password" : trainer_password,
            "trainer_join_date" : trainer_join_date,
            "status": status,
            **BaseSchema.timestamps()
        }


class PaymentSchema(BaseSchema):

    @staticmethod
    def create_payment(
        *,
        org_id,
        member_id,
        member_name : str,
        amount: float,
        payment_method: str,
        payment_date,
        status: str = "Paid"
    ) -> Dict:

        return {
            "org_id": org_id,                 # 🔗
            "member_id": member_id,           # 🔗 Member reference
            "member_name" : member_name,
            "amount": amount,
            "payment_method": payment_method,
            "payment_date": payment_date,
            "status": status,
            **BaseSchema.timestamps()
        }

